def test_count_events(test_log,run_analyzer): # TC-01
    report,scripts,test = test_log
    with open(test,'w') as f:
        f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
        f.write('2026-02-12 13:31:32 | ERROR | any text')

    
    result = run_analyzer(path = (scripts,test))

    with open(report,'r') as f:
        copy_rep = f.read()

    assert 'EVENTS  : 2' in copy_rep


def test_incorrect_file(test_log,run_analyzer): # TC-02
        report,scripts,test = test_log
        with open(test,'w') as f:
            f.write('TEST  DEBUG | TEST\n')
            f.write('2026-02-12 13:31:32 | ERROR | any text')

        result = run_analyzer(path = (scripts,test))
        assert 'UNKNOWN' in result.stdout
        assert 'UNKNOWN : 1' in result.stdout
    


def test_analyze_detail(test_log,run_analyzer): # TC-03
        report,scripts,test = test_log
        with open(test,'w') as f:
            f.write('2026-02-12 13:31:32 | ERROR | any text\n')
            f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
            f.write('2026-02-12 12:59:03 | WARN  | High CPU usage\n')
            f.write('2026-02-12 13:16:22 | INFO  | User logged out\n')
            f.write('2026-02-12 13:56:01 | FATAL | Program crash\n')

        result = run_analyzer(path = (scripts,test),flags = ['-d'])
        print(result.stdout)
        lines = result.stdout.splitlines()
        total_lines = len(lines)
        assert 'EVENTS  : 5' in result.stdout
        assert total_lines == 15
    


def test_incorrect_type_file(test_log,run_analyzer): # TC-04
        report,scripts,test = test_log
        with open(test,'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
        result = run_analyzer(path = (scripts,test))
        result = result.stdout
        assert '[Error] Unsupported file encoding or binary format' in result
     


def test_empty_file(test_log,run_analyzer): # TC-05
        report,scripts,test = test_log
        with open(test,'w') as f:
            f.write('\n')
            

        result = run_analyzer(path = (scripts,test))
        result = result.stdout
        assert '«Check file or file path»' in result
  


def test_many_logs(test_log,run_analyzer): # TC-06
        report,scripts,test = test_log
        with open(test,'w') as f:
            for i in range(1,201):
                f.write('2026-02-12 13:31:32 | ERROR | any text\n')
                f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
                f.write('2026-02-12 12:59:03 | WARN  | High CPU usage\n')
                f.write('2026-02-12 13:16:22 | INFO  | User logged out\n')
                f.write('2026-02-12 13:56:01 | FATAL | Program crash\n')
        result = run_analyzer(path = (scripts,test))
        
        lines = result.stdout.splitlines()
        total_lines = len(lines)
        assert 'EVENTS  : 1000' in result.stdout
   


def test_nonexistent_file(test_log,run_analyzer): # TC-07
    report,scripts,test = test_log
    test = 'non_existent.txt'
    result = run_analyzer(path = (scripts,test))
    assert '«Error: Path is not a file»' in result.stdout  
