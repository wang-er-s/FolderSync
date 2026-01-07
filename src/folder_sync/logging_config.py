"""日志配置模块

提供统一的日志配置，支持控制台和文件输出。
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# 默认日志格式
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志级别映射
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: str = DEFAULT_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
) -> logging.Logger:
    """配置应用程序日志

    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 可选的日志文件路径
        format_string: 日志格式字符串
        date_format: 日期格式字符串

    Returns:
        配置好的根日志记录器
    """
    # 获取根日志记录器
    root_logger = logging.getLogger("folder_sync")
    
    # 清除现有处理器
    root_logger.handlers.clear()
    
    # 设置日志级别
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    root_logger.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(format_string, date_format)
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file is not None:
        # 确保日志目录存在
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志记录器

    Args:
        name: 日志记录器名称，通常使用模块名

    Returns:
        日志记录器实例
    """
    return logging.getLogger(f"folder_sync.{name}")
