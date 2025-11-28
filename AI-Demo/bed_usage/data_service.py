import os
import time
import threading
import pandas as pd
import subprocess
import sys
import traceback
from configs.logger import get_logger
from caches.cache_manager import (
    _cache,
    is_excel_updated,
    is_cache_newer_than_excel,
    save_cache_to_file,
    load_cache_from_file,
    BASE_DIR,
    EXCEL_FILE,
    CACHE_FILE,
    METADATA_FILE
)

logger = get_logger(__name__)

# 使用缓存机制读取Excel数据
def load_data(force_reload=False):
    """读取Excel数据，并缓存以提高性能"""
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
    """
    预先计算各种聚合数据并缓存
    ✔ 读取 Excel
    ✔ 聚合统计数据
    ✔ 生成各种 API 使用的数据结构（医院、科室、热力图）
    ✔ 写入缓存文件
    ✔ 更新内存缓存 _cache
    """

    # -----------------------------
    # 1. 避免重复计算（并发锁）
    # -----------------------------
    if _cache['precomputing'] and not force_recompute:
        logger.info("已有正在进行的预计算，跳过")
        return

    _cache['precomputing'] = True  # 上锁

    try:
        # -----------------------------------------------------
        # 2. 缓存判断逻辑
        # -----------------------------------------------------
        if not force_recompute:
            cache_loaded = False

            # （1）优先：缓存文件比 Excel 新 → 缓存绝对可信
            if is_cache_newer_than_excel(EXCEL_FILE, CACHE_FILE, logger):
                cache_loaded = load_cache_from_file(CACHE_FILE, logger)

            # （2）否则：Excel 没更新 → 缓存仍然有效
            elif not is_excel_updated(EXCEL_FILE, logger):
                cache_loaded = load_cache_from_file(CACHE_FILE, logger)

            # （3）缓存加载成功 → 直接返回
            if cache_loaded:
                logger.info("缓存有效，直接使用缓存数据，无需重新计算")
                _cache['precomputing'] = False
                _cache['ready'] = True
                return

        # -----------------------------------------------------
        # 3. 需要重新计算（执行完整的预计算流程）
        # -----------------------------------------------------
        logger.info("重新计算聚合数据...")
        start_time = time.time()

        df = load_data(force_recompute)
        print(f'{df} << 数据')
        data_changed = False
        print(f'{data_changed} << 数据是否变化')

        # -----------------------------
        # 3.1 概览（Summary）优先计算
        # -----------------------------
        total_beds = df['total_beds'].sum()
        occupied_beds = df['occupied_beds'].sum()
        available_beds = df['available_beds'].sum()
        overall_occupancy_rate = (occupied_beds / total_beds * 100).round(2)

        _cache['summary_data'] = {
            'total_beds': int(total_beds),
            'occupied_beds': int(occupied_beds),
            'available_beds': int(available_beds),
            'occupancy_rate': float(overall_occupancy_rate),
            'top_departments': {'names': [], 'values': []}
        }

        # -----------------------------
        # 3.2 医院使用率
        # -----------------------------
        if _cache['hospital_usage'] is None or force_recompute:
            hospital_usage = df.groupby(['hospital_name']).agg({
                'occupied_beds': 'sum',
                'total_beds': 'sum',
                'available_beds': 'sum'
            }).reset_index()

            hospital_usage['occupancy_rate'] = (
                hospital_usage['occupied_beds'] /
                hospital_usage['total_beds'] * 100
            ).round(2)

            hospital_usage = hospital_usage.sort_values(
                by='occupancy_rate', ascending=False)

            _cache['hospital_usage'] = {
                'hospital': hospital_usage['hospital_name'].tolist(),
                'occupancy_rate': hospital_usage['occupancy_rate'].tolist(),
                'available_beds': hospital_usage['available_beds'].tolist(),
                'total_beds': hospital_usage['total_beds'].tolist()
            }
            data_changed = True

        # -----------------------------
        # 3.3 科室使用率
        # -----------------------------
        if _cache['department_usage'] is None or force_recompute:
            dept_usage = df.groupby(['department_name']).agg({
                'occupied_beds': 'sum',
                'total_beds': 'sum',
                'available_beds': 'sum'
            }).reset_index()

            dept_usage['occupancy_rate'] = (
                dept_usage['occupied_beds'] /
                dept_usage['total_beds'] * 100
            ).round(2)

            main_depts = dept_usage.sort_values(
                by='total_beds', ascending=False).head(10)

            _cache['department_usage'] = {
                'department': main_depts['department_name'].tolist(),
                'occupancy_rate': main_depts['occupancy_rate'].tolist(),
                'available_beds': main_depts['available_beds'].tolist(),
                'total_beds': main_depts['total_beds'].tolist()
            }
            data_changed = True

        # -----------------------------
        # 3.4 Summary - 科室空闲床位 TOP5
        # -----------------------------
        if force_recompute or not _cache['summary_data']['top_departments']['names']:
            dept_free_beds = df.groupby('department_name')['available_beds'].sum().reset_index()
            top_free_beds = dept_free_beds.sort_values(
                by='available_beds', ascending=False).head(5)

            _cache['summary_data']['top_departments'] = {
                'names': top_free_beds['department_name'].tolist(),
                'values': top_free_beds['available_beds'].tolist()
            }
            data_changed = True

        # -----------------------------
        # 3.5 热力图（最耗时）
        # -----------------------------
        if _cache['heatmap_data'] is None or force_recompute:
            hospital_dept = df.groupby(['hospital_name', 'department_name']).agg({
                'occupied_beds': 'sum',
                'total_beds': 'sum'
            }).reset_index()

            hospital_dept['occupancy_rate'] = (
                hospital_dept['occupied_beds'] /
                hospital_dept['total_beds'] * 100
            ).round(2)

            top_hospitals = df.groupby('hospital_name')['total_beds'].sum().nlargest(8).index.tolist()
            common_depts = ['内科', '外科', '儿科', '妇产科', '骨科', '康复科', '神经科']

            filtered = hospital_dept[
                (hospital_dept['hospital_name'].isin(top_hospitals)) &
                (hospital_dept['department_name'].isin(common_depts))
            ]

            heatmap_data = [
                [
                    top_hospitals.index(row['hospital_name']),
                    common_depts.index(row['department_name']),
                    row['occupancy_rate']
                ]
                for _, row in filtered.iterrows()
            ]

            _cache['heatmap_data'] = {
                'hospitals': top_hospitals,
                'departments': common_depts,
                'data': heatmap_data
            }
            data_changed = True

        # -----------------------------
        # 3.6 保存缓存文件
        # -----------------------------
        if data_changed:
            save_cache_to_file(CACHE_FILE, METADATA_FILE, logger)

        logger.info(f"数据计算完成，耗时: {time.time() - start_time:.2f} 秒")
        _cache['ready'] = True

    except Exception as e:
        logger.error(f"预计算数据时发生错误: {e}")

    finally:
        _cache['precomputing'] = False  # 解锁

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
    logger.info(f"try_run_precompute_script: {precompute_script}")
    logger.info(f"Excel文件: {EXCEL_FILE}")

    # 检查Excel文件是否存在
    if not os.path.exists(EXCEL_FILE):
        logger.error("Excel文件不存在，无法启动预计算")
        return False

    # 检查预计算脚本是否存在
    if not os.path.exists(precompute_script):
        logger.error(f"预计算脚本 {precompute_script} 不存在")
        return False

    try:
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
        logger.error(traceback.format_exc())  # 打印详细堆栈跟踪

    return False

