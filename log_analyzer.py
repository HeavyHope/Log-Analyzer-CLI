from pathlib import Path

file_path = Path(__file__).parent / 'dates.log'

logs = []

with open(file_path, 'r') as file:
    for i in file:
        if i.strip():
            logs.append(i)

def count_logs(logs):
    count = len(logs)
    total = f"\nEvents : {count}\n"
    count_values = {"DEBUG":0, "INFO":0, "WARN":0,
                    "ERROR":0, "FATAL":0, "UNKNOWN": 0}
    for log_lvl in logs:
        if "DEBUG" in log_lvl: count_values["DEBUG"] += 1
        elif "INFO" in log_lvl: count_values["INFO"] += 1
        elif "WARN" in log_lvl: count_values["WARN"] += 1
        elif "ERROR" in log_lvl: count_values["ERROR"] += 1
        elif "FATAL" in log_lvl: count_values["FATAL"] += 1
        else: count_values['UNKNOWN'] += 1
    print(total)
    for i in count_values:
        if count_values[i] != 0:
            print(f"{i.ljust(6)} : {count_values[i]}")

count_logs(logs)