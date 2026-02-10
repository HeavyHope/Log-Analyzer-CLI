from pathlib import Path
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-f",'--file',help='input file name with logs',
                    default = 'dates.log')
parser.add_argument('-d','--detail',help = 'show all logs',action='store_true')
args = parser.parse_args()
logs_file = args.file



file_path = Path(logs_file)

logs = []
if file_path.exists():
    if file_path.is_file():
        with open(file_path, 'r') as file:
            for i in file:
                if i.strip():
                    logs.append(i)

else: 
    print('«Error: Path is not a file»')
    exit()

def count_logs(logs):
    count = len(logs)
    total = f"\n{"EVENTS".ljust(7)} : {count}\n"
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
            print(f"{i.ljust(7)} : {count_values[i]}")
    
    with open("report.txt", 'w') as f: # create statistics file
        f.write(f"{total.strip()}\n\n")
        for i in count_values:
            if count_values[i] != 0:
                f.write(f"{i.ljust(7)} : {count_values[i]}\n")
        f.write(f"\nLOGS:\n")
        for i in logs:
            f.write(f"\n{i.strip()}")
        

if logs:
    count_logs(logs)
else:
    print('«Check file or file path»')


if args.detail: # logic for show all logs
    for i in logs:
        print(i.strip())