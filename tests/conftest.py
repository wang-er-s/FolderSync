"""Pytest 配置和共享 fixtures"""

import pytest
from pathlib import Path
import tempfile
import shutil
from typing import Generator


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """创建临时目录用于测试"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # 清理临时目录
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def source_dir(temp_dir: Path) -> Path:
    """创建源目录"""
    source = temp_dir / "source"
    source.mkdir()
    return source


@pytest.fixture
def target_dir(temp_dir: Path) -> Path:
    """创建目标目录"""
    target = temp_dir / "target"
    target.mkdir()
    return target
