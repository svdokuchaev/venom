# Модуль для работы с терминалом - логи, хоткеи, etc.

from datetime import datetime


def log(message, end='\n'):
    dt = datetime.strftime(datetime.now(), '%H:%M:%S')
    print(f'{dt} - {message}', end=end, flush=True)


def log_start(message):
    log(message, end='')


def log_add(message):
    print(message, end='', flush=True)


def log_end():
    print(flush=True)