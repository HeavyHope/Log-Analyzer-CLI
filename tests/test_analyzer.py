import subprocess
from pathlib import Path

report_path = Path(__file__).parent.parent / 'report.txt'
test_log_path = Path(__file__).parent / 'test_logs.log'
scripts_path = report_path.parent / 'log_analyzer.py'

def test_count_events():
    with open(test_log_path,'w') as f:
        f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
        f.write('2026-02-12 13:31:32 | ERROR | any text')

    subprocess.run(['py',scripts_path,'-f',test_log_path])

    with open(report_path,'r') as f:
        copy_rep = f.read()

    assert 'EVENTS  : 2' in copy_rep
    report_path.unlink()
    test_log_path.unlink()