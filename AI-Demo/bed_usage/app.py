from flask import Flask, render_template, jsonify
import time
import os
import threading
from datetime import datetime
from configs.logger import setup_logging, get_logger
from caches.cache_manager import (
    _cache, load_cache_from_file, is_cache_newer_than_excel,
    BASE_DIR, CACHE_FILE, EXCEL_FILE
)
from data_service import (
    load_data, precompute_data, async_precompute, try_run_precompute_script
)

# -----------------------------日志---------------------------------
setup_logging()
logger = get_logger(__name__)

# -----------------------------Flask应用---------------------------------

app = Flask(__name__)

# -----------------------------路由定义---------------------------------

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
