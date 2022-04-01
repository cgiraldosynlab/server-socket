import logging
import os
import datetime
from models.log import (LogApp)

class LogSys:

    def __init__(self, **args):
        try:
            args_var = os.environ
            #for item in dict(args_var):
            #    print(item, ':', args_var[item])
            logging.basicConfig(filename='log/log.log', encoding='utf-8', level=logging.DEBUG)
        except Exception as e:
            print('error:', e)

    def error(self, message, app=None) -> None:
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if app is not None:
            msg = f'{fecha} | {app} | {message}'
            LogApp(codigo=app, mensaje=f'ERROR | {msg}')
        else:
            msg = f'{fecha} | {message}'
            LogApp(codigo='python', mensaje=f'ERROR | {msg}')
        logging.error(f'ERROR | {msg}')
        print(f'ERROR | {msg}')

    def info(self, message, app=None) -> None:
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if app is not None:
            msg = f'{fecha} | {app} | {message}'
            LogApp(codigo=app, mensaje=f'INFO | {msg}')
        else:
            msg = f'{fecha} | {message}'
            LogApp(codigo='python', mensaje=f'INFO | {msg}')
        logging.error(f'INFO | {msg}')
        #print(f'INFO | {msg}')

    def warn(self, message, app=None) -> None:
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if app is not None:
            msg = f'{fecha} | {app} | {message}'
            LogApp(codigo=app, mensaje=f'WARN | {msg}')
        else:
            msg = f'{fecha} | {message}'
            LogApp(codigo='python', mensaje=f'WARN | {msg}')
        logging.warning(f'WARNING | {msg}')
        print(f'WARNING | {msg}')