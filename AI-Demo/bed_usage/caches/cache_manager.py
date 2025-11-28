import os
import json
import pickle
import hashlib
from datetime import datetime

# 全局缓存变量
_cache = {
    'data': None,
    'hospital_usage': None,  # web数据 -> 各医院使用率
    'department_usage': None,  # 科室数据 -> 各科室使用率
    'heatmap_data': None,  # 热力图数据 -> 医院科室使用率
    'summary_data': None,  # 概览数据 -> 空闲病床数量汇总
    'timestamp': 0,  # 时间戳 -> 数据更新时间
    'cache_ttl': 300,  # 缓存时间(秒)，5分钟
    'excel_last_modified': 0,  # Excel文件最后修改时间
    'excel_md5': '',  # Excel文件的MD5值 -> 文件内容校验
    'precomputing': False,  # 标记是否正在预计算 -> 防止频发触发计算任务
    'ready': False,  # 标记所有数据是否准备就绪 -> 标记所有数据是否准备就绪，避免重复计算
}

def init_cache_paths(base_dir):
    """
    初始化缓存路径
    :param base_dir: 基准目录
    :return: 包含路径信息的字典
    """
    cache_dir = os.path.join(base_dir, 'caches')
    print(f'{cache_dir} << 缓存文件目录')
    # 确保缓存目录存在
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return {
        'CACHE_DIR': cache_dir,
        'CACHE_FILE': os.path.join(cache_dir, 'data_cache.pkl'),
        'METADATA_FILE': os.path.join(cache_dir, 'metadata.json')
    }

def get_file_md5(filepath, logger=None):
    """计算文件的MD5哈希值"""
    try:
        md5_hash = hashlib.md5()
        with open(filepath, "rb") as f:
            # 读取文件块并更新哈希
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except Exception as e:
        if logger:
            logger.error(f"计算MD5异常: {e}")
        return ""

def is_excel_updated(excel_file, logger=None):
    """检查Excel文件是否有更新"""
    try:
        # 获取当前文件修改时间和MD5
        current_mtime = os.path.getmtime(excel_file)
        current_md5 = get_file_md5(excel_file, logger)

        # 如果修改时间或MD5与缓存不同，则文件已更新
        if (current_mtime != _cache['excel_last_modified'] or
            current_md5 != _cache['excel_md5']):
            _cache['excel_last_modified'] = current_mtime
            _cache['excel_md5'] = current_md5
            return True
        return False
    except Exception as e:
        if logger:
            logger.error(f"检查文件更新异常: {e}")
        return True  # 出错时假设文件已更新，重新加载数据

def is_cache_newer_than_excel(excel_file, cache_file, logger=None):
    """检查缓存文件是否比Excel文件更新（即缓存是最新的）"""
    try:
        if not os.path.exists(excel_file) or not os.path.exists(cache_file):
            return False

        excel_time = os.path.getmtime(excel_file)
        cache_time = os.path.getmtime(cache_file)

        # 缓存文件修改时间晚于Excel文件，说明缓存是最新的
        return cache_time > excel_time
    except Exception as e:
        if logger:
            logger.error(f"比较文件时间异常: {e}")
        return False

def save_cache_to_file(cache_file, metadata_file, logger=None):
    """将计算结果保存到本地文件"""
    try:
        with open(cache_file, 'wb') as f:
            # 只保存必要的数据，不包括原始DataFrame
            cache_to_save = {
                'hospital_usage': _cache['hospital_usage'],
                'department_usage': _cache['department_usage'],
                'heatmap_data': _cache['heatmap_data'],
                'summary_data': _cache['summary_data'],
                'timestamp': _cache['timestamp'],
                'excel_last_modified': _cache['excel_last_modified'],
                'excel_md5': _cache['excel_md5']
            }
            pickle.dump(cache_to_save, f)

        # 保存元数据到JSON文件
        metadata = {
            'excel_md5': _cache['excel_md5'],
            'excel_last_modified': _cache['excel_last_modified'],
            'computation_time': _cache['timestamp'],
            'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        if logger:
            logger.info(f"缓存已保存到 {cache_file}")
    except Exception as e:
        if logger:
            logger.error(f"保存缓存异常: {e}")

def load_cache_from_file(cache_file, logger=None):
    """从本地文件加载缓存数据"""
    try:
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)

                # 更新全局缓存
                _cache.update(cache_data)

                if all(key in _cache and _cache[key] is not None for key in
                      ['hospital_usage', 'department_usage', 'heatmap_data', 'summary_data']):
                    _cache['ready'] = True

                if logger:
                    logger.info(f"从文件加载缓存成功，数据时间戳: {datetime.fromtimestamp(_cache['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
                return True
        return False
    except Exception as e:
        if logger:
            logger.error(f"加载缓存异常: {e}")
        return False

