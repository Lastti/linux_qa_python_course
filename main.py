import datetime
import subprocess


def psaux_run():
    """Run ps aux command"""
    result = []
    out = subprocess.check_output(["ps", "aux"]).decode('utf-8').split('\n')
    info = out[1:-1]
    for line in info:
        process_info = line.split()
        process_data = {
            'user': process_info[0],
            'pid': int(process_info[1]),
            'cpu': float(process_info[2]),
            'vsz': float(process_info[4]),
            'command': process_info[10]
        }
        result.append(process_data)
    return result


def get_users(data):
    """Get users list from ps aux result"""
    users = []
    for line in data:
        if line['user'] not in users:
            users.append(line['user'])
    return users


def count_processes_amount(data):
    """Get processes amount from ps aux result"""
    number = 0
    processes_list = []
    for line in data:
        if line['pid'] not in processes_list:
            number += 1
    return number


def get_users_with_proc(data):
    """Get users with summ of their processes from ps aux result"""
    users = get_users(data)
    count = 0
    result = []
    for user in users:
        for line in data:
            if line['user'] == user:
                count += 1
        result.append((user, count))
    return result


def get_used_memory(data):
    """Get used memory from ps aux result"""
    summ = 0
    for line in data:
        summ += line['vsz']
    return round((summ / 1024 ** 2), 2)


def get_used_cpu(data):
    """Get used cpu from ps aux result"""
    cpu = 0
    for line in data:
        cpu += line['cpu']
    return round(cpu, 2)


def get_greedy_memory_process(data):
    """Get process uses maximum memory from ps aux result"""
    max = 0
    process_name = ''
    for line in data:
        if max < line['vsz']:
            max = line['vsz']
            process_name = line['command']
    return process_name


def get_greedy_cpu_process(data):
    """Get process uses maximum cpu from ps aux result"""
    max = 0
    process_name = ''
    for line in data:
        if max < line['cpu']:
            max = line['cpu']
            process_name = line['command']
    return process_name


psaux_result = psaux_run()
users = get_users(psaux_result)
processes_amount = count_processes_amount(psaux_result)
users_with_proc = get_users_with_proc(psaux_result)
used_memory = get_used_memory(psaux_result)
used_cpu = get_used_cpu(psaux_result)
greedy_memory_process = get_greedy_memory_process(psaux_result)
greedy_cpu_process = get_greedy_cpu_process(psaux_result)

report = f'Отчeт о состоянии системы:\n' \
         f'Пользователи системы: {" , ".join(user for user in users)}\n' \
         f'Процессов запущено: {processes_amount}\n' \
         f'Пользовательских процессов:\n' \
         f'{chr(10).join(f"{item[0]}: {item[1]}" for item in users_with_proc)}\n' \
         f'Всего памяти используется: {used_memory} mb\n' \
         f'Всего CPU используется: {used_cpu} %\n' \
         f'Больше всего памяти использует: {greedy_memory_process[0:20]}\n' \
         f'Больше всего CPU использует: {greedy_cpu_process[0:20]}\n'

print(report)

file_name = datetime.datetime.now().strftime('%d-%m-%Y-%H:%M')
with open(f'{file_name}.txt', 'w') as f:
    f.write(report)
