import pytest
from pathlib import Path
import subprocess

@pytest.fixture
def test_log():
    report_path = Path(__file__).parent.parent / 'report.txt'
    scripts_path = report_path.parent / 'log_analyzer.py'
    test_log_path = Path(__file__).parent / 'test_logs.log'
    yield report_path,scripts_path,test_log_path
    test_log_path.unlink(missing_ok=True)
    report_path.unlink(missing_ok=True)

@pytest.fixture
def run_analyzer():
    def wrapper(path : tuple, flags:list = None):
        command = ['py',path[0],'-f',path[1]]
        if flags:
            command.extend(flags)
        return subprocess.run(command, capture_output=True, text=True)
    yield wrapper