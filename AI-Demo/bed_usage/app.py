from flask import Flask, render_template, jsonify
import pandas as pd
import time
import os
import threading
from datetime import datetime
from configs.logger import setup_logging, get_logger
from caches.cache_manager import (
    _cache, init_cache_paths, is_excel_updated, is_cache_newer_than_excel,
    save_cache_to_file, load_cache_from_file
)

# 统一基准目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------日志---------------------------------
setup_logging()
logger = get_logger(__name__)

# -----------------------------Flask应用---------------------------------

app = Flask(__name__)

# -----------------------------全局缓存变量---------------------------------
# 初始化缓存路径
cache_paths = init_cache_paths(BASE_DIR)
CACHE_DIR = cache_paths['CACHE_DIR']
CACHE_FILE = cache_paths['CACHE_FILE']
METADATA_FILE = cache_paths['METADATA_FILE']
EXCEL_FILE = os.path.join(BASE_DIR, 'hospital_bed_usage_data.xlsx')

# 使用缓存机制读取Excel数据
def load_data(force_reload=False):
    """读取Excel数据，并缓存以提高性能"""
    global _cache
    current_time = time.time()

    # 检查是否需要重新加载数据
    need_reload = (
        _cache['data'] is None or  # 没有数据
        force_reload or  # 强制刷新
        is_excel_updated(EXCEL_FILE, logger) or  # Excel文件已更新
        current_time - _cache['timestamp'] > _cache['cache_ttl']  # 缓存过期
    )

    if need_reload:
        logger.info("重新加载Excel数据...")
        df = pd.read_excel(EXCEL_FILE)
        _cache['data'] = df
        _cache['timestamp'] = current_time
        # 清除其他缓存
        _cache['hospital_usage'] = None
        _cache['department_usage'] = None
        _cache['heatmap_data'] = None
        _cache['summary_data'] = None
        _cache['ready'] = False

    return _cache['data']

# 提前计算和缓存聚合数据
def precompute_data(force_recompute=False):
    """预先计算各种聚合数据并缓存"""
    global _cache

    # 避免重复计算
    if _cache['precomputing'] and not force_recompute:
        logger.info("已有正在进行的预计算，跳过")
        return

    _cache['precomputing'] = True

    try:
        # 检查是否可以使用预先计算好的缓存文件
        if not force_recompute and is_cache_newer_than_excel(EXCEL_FILE, CACHE_FILE, logger):
            if load_cache_from_file(CACHE_FILE, logger):
                logger.info("使用预先计算的缓存数据，无需重新计算")
                _cache['precomputing'] = False
                _cache['ready'] = True
                return

        # 如果缓存为空且未强制重新计算，尝试从文件加载
        if (not force_recompute and
            _cache['hospital_usage'] is None and
            _cache['department_usage'] is None):
            if load_cache_from_file(CACHE_FILE, logger):
                # 检查Excel文件是否更新，如果没更新直接使用缓存
                if not is_excel_updated(EXCEL_FILE, logger):
                    logger.info("使用文件缓存数据，Excel未更新")
                    _cache['precomputing'] = False
                    _cache['ready'] = True
                    return

        # 需要重新计算
        logger.info("重新计算聚合数据...")
        start_time = time.time()
        df = load_data(force_recompute)
        data_changed = False

        # 快速计算概览数据（优先显示）
        total_beds = df['total_beds'].sum()
        occupied_beds = df['occupied_beds'].sum()
        available_beds = df['available_beds'].sum()
        overall_occupancy_rate = (occupied_beds / total_beds * 100).round(2)

        _cache['summary_data'] = {
            'total_beds': int(total_beds),
            'occupied_beds': int(occupied_beds),
            'available_beds': int(available_beds),
            'occupancy_rate': float(overall_occupancy_rate),
            'top_departments': {'names': [], 'values': []}  # 先用空数据
        }

        # 计算医院使用率数据
        if _cache['hospital_usage'] is None or force_recompute:
            hospital_usage = df.groupby(['hospital_name']).agg({
                'occupied_beds': 'sum',
                'total_beds': 'sum',
                'available_beds': 'sum'
            }).reset_index()

            hospital_usage['occupancy_rate'] = (hospital_usage['occupied_beds'] / hospital_usage['total_beds'] * 100).round(2)
            hospital_usage = hospital_usage.sort_values(by='occupancy_rate', ascending=False)

            _cache['hospital_usage'] = {
                'hospital': hospital_usage['hospital_name'].tolist(),
                'occupancy_rate': hospital_usage['occupancy_rate'].tolist(),
                'available_beds': hospital_usage['available_beds'].tolist(),
                'total_beds': hospital_usage['total_beds'].tolist()
            }
            data_changed = True

        # 计算科室使用率数据
        if _cache['department_usage'] is None or force_recompute:
            dept_usage = df.groupby(['department_name']).agg({
                'occupied_beds': 'sum',
                'total_beds': 'sum',
                'available_beds': 'sum'
            }).reset_index()

            dept_usage['occupancy_rate'] = (dept_usage['occupied_beds'] / dept_usage['total_beds'] * 100).round(2)
            main_depts = dept_usage.sort_values(by='total_beds', ascending=False).head(10)

            _cache['department_usage'] = {
                'department': main_depts['department_name'].tolist(),
                'occupancy_rate': main_depts['occupancy_rate'].tolist(),
                'available_beds': main_depts['available_beds'].tolist(),
                'total_beds': main_depts['total_beds'].tolist()
            }
            data_changed = True

        # 计算剩余的概览数据 - 科室空闲病床数
        if force_recompute or not _cache['summary_data']['top_departments']['names']:
            dept_free_beds = df.groupby('department_name')['available_beds'].sum().reset_index()
            top_free_beds_depts = dept_free_beds.sort_values(by='available_beds', ascending=False).head(5)

            _cache['summary_data']['top_departments'] = {
                'names': top_free_beds_depts['department_name'].tolist(),
                'values': top_free_beds_depts['available_beds'].tolist()
            }
            data_changed = True

        # 计算热力图数据 (最耗时的操作放在最后)
        if _cache['heatmap_data'] is None or force_recompute:
            hospital_dept_usage = df.groupby(['hospital_name', 'department_name']).agg({
                'occupied_beds': 'sum',
                'total_beds': 'sum'
            }).reset_index()

            hospital_dept_usage['occupancy_rate'] = (hospital_dept_usage['occupied_beds'] / hospital_dept_usage['total_beds'] * 100).round(2)

            top_hospitals = df.groupby('hospital_name')['total_beds'].sum().nlargest(8).index.tolist()
            common_depts = ['内科', '外科', '儿科', '妇产科', '骨科', '康复科', '神经科']

            filtered_data = hospital_dept_usage[
                (hospital_dept_usage['hospital_name'].isin(top_hospitals)) &
                (hospital_dept_usage['department_name'].isin(common_depts))
            ]

            heatmap_data = []
            for _, row in filtered_data.iterrows():
                if row['hospital_name'] in top_hospitals and row['department_name'] in common_depts:
                    heatmap_data.append([
                        top_hospitals.index(row['hospital_name']),
                        common_depts.index(row['department_name']),
                        row['occupancy_rate']
                    ])

            _cache['heatmap_data'] = {
                'hospitals': top_hospitals,
                'departments': common_depts,
                'data': heatmap_data
            }
            data_changed = True

        # 如果数据有变化，保存到文件
        if data_changed:
            save_cache_to_file(CACHE_FILE, METADATA_FILE, logger)

        end_time = time.time()
        logger.info(f"数据计算完成，耗时: {end_time - start_time:.2f} 秒")
        _cache['ready'] = True

    except Exception as e:
        logger.error(f"预计算数据时发生错误: {e}")

    finally:
        _cache['precomputing'] = False

# 异步预计算数据
def async_precompute():
    """在后台线程中预计算数据"""
    thread = threading.Thread(target=precompute_data)
    thread.daemon = True
    thread.start()
    logger.info("启动后台数据预计算线程")

# 尝试运行预计算脚本
def try_run_precompute_script():
    """尝试运行独立的预计算脚本"""
    precompute_script = os.path.join(BASE_DIR, 'precompute_data.py')

    # 检查Excel文件是否存在
    if not os.path.exists(EXCEL_FILE):
        logger.error("Excel文件不存在，无法启动预计算")
        return False

    # 检查预计算脚本是否存在
    if not os.path.exists(precompute_script):
        logger.error(f"预计算脚本 {precompute_script} 不存在")
        return False

    try:
        import subprocess
        import sys

        # 获取当前Python解释器路径
        python_executable = sys.executable
        logger.info(f"使用Python解释器: {python_executable}")
        logger.info(f"启动预计算脚本: {precompute_script}")

        # 使用当前Python解释器运行脚本
        process = subprocess.Popen(
            [python_executable, precompute_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # 使用文本模式，方便读取输出
        )

        # 获取一些初始输出进行记录
        try:
            stdout, stderr = process.communicate(timeout=2)
            if stdout:
                logger.info(f"预计算脚本输出: {stdout[:200]}...")
            if stderr:
                logger.error(f"预计算脚本错误: {stderr}")
        except subprocess.TimeoutExpired:
            # 正常情况，脚本会继续在后台运行
            pass

        return True
    except Exception as e:
        logger.error(f"运行预计算脚本异常: {e}")
        import traceback
        logger.error(traceback.format_exc())  # 打印详细堆栈跟踪

    return False

@app.route('/')
def index():
    # 只检查是否有缓存，如无则启动异步预计算
    if not _cache['ready']:
        # 先尝试从文件加载缓存
        if not load_cache_from_file(CACHE_FILE, logger) or not _cache['ready']:
            # 如果加载失败或缓存不完整，启动异步预计算
            async_precompute()

    return render_template('index.html', ready=_cache['ready'])

@app.route('/api/hospital_usage')
def hospital_usage():
    """获取各医院病床使用率数据"""
    # 如果缓存中有数据，直接返回
    if _cache['hospital_usage'] is not None:
        return jsonify(_cache['hospital_usage'])

    # 如果没有数据，先尝试从文件加载
    if not _cache['ready'] and not _cache['precomputing']:
        if load_cache_from_file(CACHE_FILE, logger) and _cache['hospital_usage'] is not None:
            return jsonify(_cache['hospital_usage'])

        # 如果仍然没有数据，启动异步计算
        async_precompute()

    # 没有数据时返回空数据结构而不是加载状态
    return jsonify({
        'hospital': [],
        'occupancy_rate': [],
        'available_beds': [],
        'total_beds': []
    })

@app.route('/api/department_usage')
def department_usage():
    """获取各科室病床使用率数据"""
    # 如果缓存中有数据，直接返回
    if _cache['department_usage'] is not None:
        return jsonify(_cache['department_usage'])

    # 如果没有数据，先尝试从文件加载
    if not _cache['ready'] and not _cache['precomputing']:
        if load_cache_from_file(CACHE_FILE, logger) and _cache['department_usage'] is not None:
            return jsonify(_cache['department_usage'])

        # 如果仍然没有数据，启动异步计算
        async_precompute()

    # 没有数据时返回空数据结构而不是加载状态
    return jsonify({
        'department': [],
        'occupancy_rate': [],
        'available_beds': [],
        'total_beds': []
    })

@app.route('/api/hospital_dept_heatmap')
def hospital_dept_heatmap():
    """获取医院科室病床使用率热力图数据"""
    # 如果缓存中有数据，直接返回
    #print('heatmap_data', _cache['heatmap_data'])
    if _cache['heatmap_data'] is not None:
        return jsonify(_cache['heatmap_data'])

    # 如果没有数据，先尝试从文件加载
    if not _cache['ready'] and not _cache['precomputing']:
        if load_cache_from_file(CACHE_FILE, logger) and _cache['heatmap_data'] is not None:
            return jsonify(_cache['heatmap_data'])

        # 如果仍然没有数据，启动异步计算
        async_precompute()

    # 没有数据时返回空数据结构而不是加载状态
    return jsonify({
        'hospitals': [],
        'departments': [],
        'data': []
    })

@app.route('/api/free_beds_summary')
def free_beds_summary():
    """获取空闲病床数量汇总数据"""
    # 如果缓存中有数据，直接返回
    if _cache['summary_data'] is not None:
        return jsonify(_cache['summary_data'])

    # 如果没有数据，先尝试从文件加载
    if not _cache['ready'] and not _cache['precomputing']:
        if load_cache_from_file(CACHE_FILE, logger) and _cache['summary_data'] is not None:
            return jsonify(_cache['summary_data'])

        # 如果仍然没有数据，启动异步计算
        async_precompute()

    # 没有数据时返回空数据结构而不是加载状态
    return jsonify({
        'total_beds': 0,
        'occupied_beds': 0,
        'available_beds': 0,
        'occupancy_rate': 0,
        'top_departments': {'names': [], 'values': []}
    })

@app.route('/api/refresh_data')
def refresh_data():
    """强制刷新数据"""
    try:
        # 强制重新加载数据和计算，使用线程避免阻塞响应
        def refresh_task():
            load_data(force_reload=True)
            precompute_data(force_recompute=True)

        threading.Thread(target=refresh_task).start()

        return jsonify({
            'status': 'success',
            'message': '数据刷新中...',
            'timestamp': _cache['timestamp'],
            'excel_modified': _cache['excel_last_modified']
        })
    except Exception as e:
        logger.error(f"刷新数据异常: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/compute_status')
def compute_status():
    """获取数据计算状态"""
    return jsonify({
        'precomputing': _cache['precomputing'],
        'ready': _cache['ready'],
        'hospital_ready': _cache['hospital_usage'] is not None,
        'department_ready': _cache['department_usage'] is not None,
        'heatmap_ready': _cache['heatmap_data'] is not None,
        'summary_ready': _cache['summary_data'] is not None,
        'timestamp': _cache['timestamp'],
        'formatted_time': datetime.fromtimestamp(_cache['timestamp']).strftime('%Y-%m-%d %H:%M:%S') if _cache['timestamp'] > 0 else ''
    })

@app.route('/api/run_precompute')
def run_precompute():
    """手动触发预计算过程"""
    success = try_run_precompute_script()
    return jsonify({
        'status': 'success' if success else 'error',
        'message': '预计算脚本已启动' if success else '无法启动预计算脚本'
    })

if __name__ == '__main__':
    # 启动应用前加载缓存数据
    logger.info("正在启动应用，尝试加载预计算数据...")
    cache_loaded = load_cache_from_file(CACHE_FILE, logger)

    if cache_loaded:
        logger.info("成功加载预计算数据，应用准备就绪")
    else:
        logger.info("未找到预计算数据或加载失败")
        # 如果缓存不是最新的，尝试运行预计算脚本
        precompute_script = os.path.join(BASE_DIR, 'precompute_data.py')
        if not is_cache_newer_than_excel(EXCEL_FILE, CACHE_FILE, logger) and os.path.exists(precompute_script):
            logger.info("尝试运行预计算脚本...")
            try_run_precompute_script()
            # 等待3秒让预计算脚本开始运行
            time.sleep(3)
            # 再次尝试加载缓存
            cache_loaded = load_cache_from_file(CACHE_FILE, logger)
            if cache_loaded:
                logger.info("预计算数据已加载，应用准备就绪")

    # 如果缓存仍不完整，启动应用前进行异步预计算
    if not _cache['ready']:
        logger.info("应用启动前预计算数据...")
        async_precompute()

    app.run(debug=True, threaded=True, port=8989)
