import os
import datetime

def get_fecha():
    #fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return fecha

def log_show(msg='', level='MESSAGE', procedure='', file=__file__):
    print(f'[+] {get_fecha()} | {file} | {procedure} | {level} | {msg}')

def get_files(path, extension='txt') -> []:
    ''' listar ficheros de una carpeta '''
    try:
        if path == '':
            return []
        return [_ for _ in os.listdir(path) if _.endswith(f'.{extension}')]
        #return os.listdir(path)
    except Exception as e:
        log_show(msg=e, level='ERROR', procedure='get_files')
        return []

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

