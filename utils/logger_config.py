import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def setup_logger():
    # 创建logs目录
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志文件路径
    log_file = log_dir / 'mapApp.log'
    
    # 创建logger
    logger = logging.getLogger('AppLogger')
    logger.setLevel(logging.DEBUG)
    
    # 创建RotatingFileHandler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=1,
        encoding='utf-8'
    )
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    
    return logger

# 创建日志记录器实例--应用共用一个实例防止重复创建
logger = setup_logger()
