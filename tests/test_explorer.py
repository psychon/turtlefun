"""src/tests/test_explorer.py"""

from loguru import logger
import os
from pathlib import Path

import filetype

import turtlefun.turtle_explorer as te
from turtlefun.turtle_explorer import explore_euler_spiral

def test_simple_single_thread(tmp_path):
    explore_euler_spiral(0.9, 1.1, 0.1, 100, 1, tmp_path)
    logger.debug("File: {}", Path(tmp_path).rglob('*.*'))
    assert len(Path(tmp_path).rglob('*.*')) == 3 * 2
    for file in Path(tmp_path).rglob('*.*'):
        if file.endswith("png"):
            assert filetype.guess(tmp_path / file).mime == "image/png"
        
def test_simple_single_thread_newpath(tmp_path):
    explore_euler_spiral(1, 1, 0.1, 100, 1, tmp_path / "result")
    logger.debug("File: {}", Path(tmp_path).rglob('*.*'))
    assert len(os.listdir(tmp_path / "result")) == 1 * 2
    for file in os.listdir(tmp_path / "result"):
        if file.endswith("png"):
            assert filetype.guess(tmp_path / "result" / file).mime == "image/png"       
        
def test_simple_single_thread_nonepath():
    te.default_path = "./pytest_path"
    explore_euler_spiral(1, 1, 0.1, 100, 1)
    logger.debug("File: {}", Path(tmp_path).rglob('*.*'))
    assert len(Path(te.default_path).rglob('*.*')) == 1 * 2
    for file in Path(te.default_path).rglob('*.*'):
        if file.endswith("png"):
            assert filetype.guess(os.path.join(te.default_path, file)).mime == "image/png"
        os.remove(os.path.join(te.default_path, file))
    os.rmdir(te.default_path)
    
def test_simple_multi_thread(tmp_path):
    explore_euler_spiral(0.1, 1.9, 0.1, 100, 3, tmp_path)
    logger.debug("File: {}", Path(tmp_path).rglob('*.*'))
    assert len(Path(tmp_path).rglob('*.*')) == 19 * 2
    for file in Path(tmp_path).rglob('*.*'):
        if file.endswith("png"):
            assert filetype.guess(tmp_path / file).mime == "image/png"
    
def test_simple_single_thread_file_exists(tmp_path):
    explore_euler_spiral(1, 1, 0.1, 100, 1, tmp_path)
    explore_euler_spiral(1, 1, 0.1, 100, 1, tmp_path)
    logger.debug("File: {}", Path(tmp_path).rglob('*.*'))
    assert len(Path(tmp_path).rglob('*.*')) == 1 * 2
    
def test_simple_single_thread_file_exists_with_different_params(tmp_path):
    explore_euler_spiral(1, 1, 0.1, 100, 1, tmp_path)
    explore_euler_spiral(1, 1, 0.1, 101, 1, tmp_path)
    logger.debug("File: {}", Path(tmp_path).rglob('*.*'))
    assert len(Path(tmp_path).rglob('*.*')) == 2 * 2