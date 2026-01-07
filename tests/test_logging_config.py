"""日志配置模块测试"""

import logging
from pathlib import Path

from folder_sync.logging_config import setup_logging, get_logger


def test_setup_logging_default() -> None:
    """测试默认日志配置"""
    logger = setup_logging()
    
    assert logger.name == "folder_sync"
    assert logger.level == logging.INFO
    assert len(logger.handlers) >= 1


def test_setup_logging_with_level() -> None:
    """测试指定日志级别"""
    logger = setup_logging(level="DEBUG")
    
    assert logger.level == logging.DEBUG


def test_setup_logging_with_file(temp_dir: Path) -> None:
    """测试日志文件输出"""
    log_file = temp_dir / "logs" / "test.log"
    logger = setup_logging(log_file=log_file)
    
    # 写入测试日志
    logger.info("测试日志消息")
    
    # 验证日志文件已创建
    assert log_file.exists()
    
    # 验证日志内容
    content = log_file.read_text(encoding="utf-8")
    assert "测试日志消息" in content
    
    # 清理：关闭所有处理器以释放文件句柄（Windows需要）
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_get_logger() -> None:
    """测试获取子日志记录器"""
    logger = get_logger("test_module")
    
    assert logger.name == "folder_sync.test_module"
