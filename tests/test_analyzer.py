import allure

@allure.feature("Анализ логов")
@allure.story("Анализ по умолчанию")
@allure.severity(allure.severity_level.CRITICAL)
def test_count_events(test_log,run_analyzer): # TC-01

    with allure.step("Подготовка тестовых логов"):
        report,scripts,test = test_log
        with open(test,'w') as f:
            f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
            f.write('2026-02-12 13:31:32 | ERROR | any text')

    with allure.step("Запуск анализатора"):
        result = run_analyzer(path = (scripts,test))

        with open(report,'r') as f:
            copy_rep = f.read()
    with allure.step('Проверка результата'):
        assert 'EVENTS  : 2' in copy_rep

@allure.feature("Анализ логов")
@allure.story("Файл неверного формата")
@allure.severity(allure.severity_level.NORMAL)
def test_incorrect_file(test_log,run_analyzer): # TC-02
        with allure.step("Подготовка тестовых логов"):
            report,scripts,test = test_log
            with open(test,'w') as f:
                f.write('TEST  DEBUG | TEST\n')
                f.write('2026-02-12 13:31:32 | ERROR | any text')
        with allure.step("Запуск анализатора"):
            result = run_analyzer(path = (scripts,test))
        with allure.step('Проверка результата'):
            assert 'UNKNOWN' in result.stdout
            assert 'UNKNOWN : 1' in result.stdout
    

@allure.feature("Анализ логов")
@allure.story("Анализ с полной детализацией")
@allure.severity(allure.severity_level.NORMAL)
def test_analyze_detail(test_log,run_analyzer): # TC-03
        with allure.step("Подготовка тестовых логов"):
            report,scripts,test = test_log
            with open(test,'w') as f:
                f.write('2026-02-12 13:31:32 | ERROR | any text\n')
                f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
                f.write('2026-02-12 12:59:03 | WARN  | High CPU usage\n')
                f.write('2026-02-12 13:16:22 | INFO  | User logged out\n')
                f.write('2026-02-12 13:56:01 | FATAL | Program crash\n')
        with allure.step("Запуск анализатора"):     
            result = run_analyzer(path = (scripts,test),flags = ['-d'])
        with allure.step("Подсчет строк выведенные в кмд"):    
            print(result.stdout)
            lines = result.stdout.splitlines()
            total_lines = len(lines)
        with allure.step('Проверка результата'):
            assert 'EVENTS  : 5' in result.stdout
            assert total_lines == 15
    

@allure.feature("Анализ логов")
@allure.story("некорректный тип файла")
@allure.severity(allure.severity_level.CRITICAL)
def test_incorrect_type_file(test_log,run_analyzer): # TC-04
        with allure.step("Подготовка тестовых логов"):
            report,scripts,test = test_log
            with open(test,'wb') as f:
                f.write(b'\x89PNG\r\n\x1a\n')
        with allure.step("Запуск анализатора"):         
            result = run_analyzer(path = (scripts,test))
            result = result.stdout
        with allure.step('Проверка результата'):
            assert'[Error] Unsupported file encoding or binary format'in result
     

@allure.feature("Анализ логов")
@allure.story("Пустой файл")
@allure.severity(allure.severity_level.CRITICAL)
def test_empty_file(test_log,run_analyzer): # TC-05
        with allure.step("Подготовка тестовых логов"):
            report,scripts,test = test_log
            with open(test,'w') as f:
                f.write('\n')
            
        with allure.step("Запуск анализатора"):
            result = run_analyzer(path = (scripts,test))
            result = result.stdout
        with allure.step('Проверка результата'):
            assert '«Check file or file path»' in result
  

@allure.feature("Анализ логов")
@allure.story("1000 логов")
@allure.severity(allure.severity_level.CRITICAL)
def test_many_logs(test_log,run_analyzer): # TC-06
        with allure.step("Подготовка тестовых логов"):
            report,scripts,test = test_log
            with open(test,'w') as f:
                for i in range(1,201):
                    f.write('2026-02-12 13:31:32 | ERROR | any text\n')
                    f.write('2026-02-12 13:14:41 | DEBUG | any text\n')
                    f.write('2026-02-12 12:59:03 | WARN  | High CPU usage\n')
                    f.write('2026-02-12 13:16:22 | INFO  | User logged out\n')
                    f.write('2026-02-12 13:56:01 | FATAL | Program crash\n')
        with allure.step("Запуск анализатора"):
            result = run_analyzer(path = (scripts,test))
            lines = result.stdout.splitlines()
            total_lines = len(lines)
        with allure.step('Проверка результата'):
            assert 'EVENTS  : 1000' in result.stdout
   

@allure.feature("Анализ логов")
@allure.story("Несуществующий файл")
@allure.severity(allure.severity_level.CRITICAL)
def test_nonexistent_file(test_log,run_analyzer): # TC-07
    with allure.step("Подготовка тестовых логов"):
        report,scripts,test = test_log
        test = 'non_existent.txt'
    with allure.step("Запуск анализатора"):
        result = run_analyzer(path = (scripts,test))
    with allure.step('Проверка результата'):
        assert '«Error: Path is not a file»' in result.stdout  
