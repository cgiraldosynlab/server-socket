import logging
import os


class LogSys:
    def __init__(self, **args):
        try:
            args_var = os.environ
            for item in dict(args_var):
                print(item, ':', args_var[item])
            logging.basicConfig(filename='./log.log', encoding='utf-8', level=logging.DEBUG)
        except Exception as e:
            print('error:', e)

log = LogSys(level='debbug', msg='Esto es una prueba')