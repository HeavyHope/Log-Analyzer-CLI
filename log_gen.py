import json
from datetime import datetime, timedelta
from pathlib import Path
import random

file_dir = Path(__file__).parent # получаем абсолютный путь до проекта
file_path = file_dir / "logs_list.json" # добавляем путь к файлу

with open(file_path, 'r') as f: # открываем файл для чтения
    data = json.load(f) # закидываем в переменную логи в качестве словаря

#генерируем дату и время для логов
def generate_datetime():
    dates = []
    now = datetime.now()
    for i in range(random.randint(50,101)):
        changed_time = now - timedelta(hours=random.randint(0,25))
        changed_time = changed_time - timedelta(minutes=random.randint(1,61))
        changed_time = changed_time - timedelta(seconds=random.randint(1,61))
        dates.append(changed_time.strftime("%Y-%m-%d %H:%M:%S"))
    dates.sort()
    return dates

#рандомим логи из заготовки и склеиваем со временем
def generate_logs(time,data):
    logs = []
    for log in range(len(time)):
        log_key,log_value = random.choice(list(data.items()))
        logs.append(f"{time[log]} | {log_key.ljust(5)} | "
                    f"{random.choice(log_value)}")
    return logs

date_time = generate_datetime()
logs = generate_logs(date_time,data)

# сохраняем наши сгенерированные логи в файл
file_path = file_dir / "dates.log"
with open(file_path, 'w') as file:
    for i in logs:
        file.write(f"{i}\n")