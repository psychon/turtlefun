"""tests/test_console.py"""

import click.testing
import os
import pytest

from turtlefun import turtlefun

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_succeeds(runner):
    result = runner.invoke(turtlefun.turtlefun)
    assert result.exit_code == 0

def test_main_version(runner):
    result = runner.invoke(turtlefun.turtlefun, ['--version'])
    assert result.exit_code == 0
    assert "turtlefun, version" in result.output

def test_speedtest(runner):
    result = runner.invoke(turtlefun.turtlefun, ["speedtest", "-i", "100", "-i", "1000"])
    assert result.exit_code == 0
    for string in ["Theta", "iterate", "steps", "draw", "time", "delta time"]:
        assert string in result.output

def test_spirale(runner, tmp_path):
    result = runner.invoke(turtlefun.turtlefun, ["spiral", "-p", str(tmp_path)])
    assert result.exit_code == 0
    assert len(os.listdir(tmp_path)) == 2 * 2
    
def test_spirale_noscale(runner, tmp_path):
    result = runner.invoke(turtlefun.turtlefun, ["spiral", "-p", str(tmp_path), "--no-scale"])
    assert result.exit_code == 0
    assert len(os.listdir(tmp_path)) == 1 * 2

def test_spirale_explorer_simple(runner, tmp_path):
    result = runner.invoke(turtlefun.turtlefun, ["explore", "-p", str(tmp_path), "-s", "0.9", "-e", "1.1", "-a", "0.1", "-i", "100"])
    assert result.exit_code == 0
    assert len(os.listdir(tmp_path)) == 3 * 2
    
def test_spirale_explorer_origin_return(runner, tmp_path):
    result = runner.invoke(turtlefun.turtlefun, ["explore", "-p", str(tmp_path), "-s", "1", "-e", "1", "-a", "0.1", "-i", "1000"])
    assert result.exit_code == 0
    assert len(os.listdir(tmp_path)) == 2 * 2
