"""Folder Sync 应用程序入口点"""

import sys
from logging_config import get_logger

logger = get_logger(__name__)


def main() -> int:
    """应用程序主入口

    Returns:
        退出代码 (0 表示成功)
    """
    logger.info("Folder Sync 启动中...")
    
    # TODO: 在后续任务中实现 GUI 启动逻辑
    logger.info("应用程序初始化完成")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
