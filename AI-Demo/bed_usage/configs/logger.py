import os
import logging
from logging.handlers import RotatingFileHandler

'''
  功能说明：
  | 功能                | 说明           |
  | ----------------- | ------------ |
  | 日志目录自动创建          | 避免运行时崩溃      |
  | 日志轮转（10MB × 5 文件） | 防止磁盘被 log 填满 |
  | 统一格式 + 时间戳        | 排查问题更清晰      |
  | 控制台 + 文件双输出       | 开发 / 生产两不误   |
  | 模块级 logger        | 精细控制日志来源     |
'''

def setup_logging():
    """
    配置并初始化日志系统
    """
    # 配置日志记录器
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    print(LOG_DIR, '<< LOG_DIR')
    os.makedirs(LOG_DIR, exist_ok=True)  # 确保日志目录存在
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')  # 日志文件路径

    # 创建日志格式器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建轮转文件处理器（单个文件最大10MB，保留5个备份文件）
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 保留5个备份文件
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )

def get_logger(name):
    """
    获取指定名称的日志记录器
    """
    return logging.getLogger(name)
