import os
import platform
import socket
from helpers import log_show

class Config:
    ''' clases que carga todas las configuraciones generales '''

    __entorno = 'develop'
    __plataform = ''
    __IP = ''
    __path_order = ''
    __enviroment = None

    def __init__(self):
        try:
            if os.environ.get('PYTHON_ENV'):
                self.__entorno = os.environ['PYTHON_ENV']
                setting = os.environ
            else:
                from dotenv import dotenv_values
                setting = dotenv_values('.env')

            if setting and setting['PYTHON_ENV']:
                self.__enviroment = setting
                self.__entorno = setting['PYTHON_ENV']
                self.__plataform  = platform.system()
                self.__path_order = setting['PATH_ORDER']

        except Exception as e:
            log_show(msg=e, level='ERROR', procedure='__init__', file=__file__)

    def extract_ip(self):
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            IP = st.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            st.close()
        return IP

    def get_env(self):
        return self.__entorno

    def get_plataform(self):
        return self.__plataform

    def get_path_order(self):
        return self.__path_order

    def get_enviroment(self):
        return self.__enviroment

    ''' declaration property '''
    entorno: str = property(get_env)
    plataforma: str = property(get_plataform)
    Ip: str = property(extract_ip)
    path_order: str = property(get_path_order)
    global_enviroment = property(get_enviroment)