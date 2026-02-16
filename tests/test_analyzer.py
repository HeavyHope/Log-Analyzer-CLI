import subprocess
from pathlib import Path

report_path = Path(__file__).parent.parent / 'report.txt'
test_log_path = Path(__file__).parent / 'test_logs.log'
scripts_path = report_path.parent / 'log_analyzer.py'

def end_delete():
    report_path.unlink(missing_ok=True)
    test_log_path.unlink(missing_ok=True)


def test_count_events(): # TC-01
    try:
        with open(test_log_path,'w') as f:
            f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
            f.write('2026-02-12 13:31:32 | ERROR | any text')

        subprocess.run(['py',scripts_path,'-f',test_log_path])

        with open(report_path,'r') as f:
            copy_rep = f.read()

        assert 'EVENTS  : 2' in copy_rep
    finally:
        end_delete()

def test_incorrect_file(): # TC-02
    try:
        with open(test_log_path,'w') as f:
            f.write('TEST  DEBUG | TEST\n')
            f.write('2026-02-12 13:31:32 | ERROR | any text')

        result = subprocess.run(['py',scripts_path,'-f',test_log_path],
                       capture_output=True,text=True)
        assert 'UNKNOWN' in result.stdout
        assert 'UNKNOWN : 1' in result.stdout
    finally:     
        end_delete()

def test_analyze_detail(): # TC-03
    try:
        with open(test_log_path,'w') as f:
            f.write('2026-02-12 13:31:32 | ERROR | any text\n')
            f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
            f.write('2026-02-12 12:59:03 | WARN  | High CPU usage\n')
            f.write('2026-02-12 13:16:22 | INFO  | User logged out\n')
            f.write('2026-02-12 13:56:01 | FATAL | Program crash\n')

        result = subprocess.run(['py',scripts_path,'-f',test_log_path,'-d'],
                       capture_output=True,text=True)
        print(result.stdout)
        lines = result.stdout.splitlines()
        total_lines = len(lines)
        assert 'EVENTS  : 5' in result.stdout
        assert total_lines == 15
    finally:     
        end_delete()

def test_incorrect_type_file(): # TC-04
    try:
        with open(test_log_path,'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
        result = subprocess.run(['py',scripts_path,'-f',test_log_path],
                       capture_output=True,text=True)
        result = result.stdout
        assert '[Error] Unsupported file encoding or binary format' in result
    finally:     
        end_delete()

def test_empty_file(): # TC-05
    try:
        with open(test_log_path,'w') as f:
            f.write('\n')
            

        result = subprocess.run(['py',scripts_path,'-f',test_log_path,],
                       capture_output=True,text=True)
        result = result.stdout
        assert '«Check file or file path»' in result
    finally:     
        end_delete()

def test_many_logs(): # TC-06
    try:
        with open(test_log_path,'w') as f:
            for i in range(1,201):
                f.write('2026-02-12 13:31:32 | ERROR | any text\n')
                f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
                f.write('2026-02-12 12:59:03 | WARN  | High CPU usage\n')
                f.write('2026-02-12 13:16:22 | INFO  | User logged out\n')
                f.write('2026-02-12 13:56:01 | FATAL | Program crash\n')
        result = subprocess.run(['py',scripts_path,'-f',test_log_path,],
                       capture_output=True,text=True)
        
        lines = result.stdout.splitlines()
        total_lines = len(lines)
        assert 'EVENTS  : 1000' in result.stdout
    finally:     
        end_delete()

def test_nonexistent_file(): # TC-07
    try:
        test_log_path = 'non_existent.txt'

        result = subprocess.run(['py',scripts_path,'-f',test_log_path],
                       capture_output=True,text=True)
        assert '«Error: Path is not a file»' in result.stdout
    finally:     
        end_delete()