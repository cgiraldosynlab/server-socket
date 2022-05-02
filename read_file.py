import os.path
import socket
import time

from config import Config
from helpers import log_show, get_files

config = Config()


class ClientSocket:
    __host: str = ''
    __port: int = 0
    __is_setting = False
    __buffer: int = 1024

    def __init__(self):
        try:
            self.__host = config.global_enviroment['SOCKET_SERVER_HOST']
            self.__port = int(config.global_enviroment['SOCKET_SERVER_PORT'])
            self.__is_setting = (True if (self.__host != '') and (self.__port > 0) else False)
            self.__buffer = (int(config.global_enviroment['SOCKET_SERVER_BUFFER']) if config.global_enviroment.get(
                'SOCKET_SERVER_BUFFER') else 1024)
        except Exception as e:
            log_show(file=__class__, msg=e, procedure='__init__', level='ERROR')

    def send_data(self, content: str) -> bool:
        try:
            if not self.__is_setting:
                return False

            if content.strip() == '':
                return False

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(30)
            client.connect((self.__host, self.__port))
            client.send(content.encode(encoding='utf-8'))
            response = client.recv(self.__buffer)
            log_show(msg=response.decode().replace(chr(11), '').replace(chr(28), ''), level='info',
                     procedure='_send_data', file=__class__)
            client.close()
            return True if response.decode() != '' else False
        except Exception as e:
            log_show(msg=e, level='error', procedure='send_data', file=__class__)
            return False


class ReadHL7:
    __path_read: str = ''
    __list: [] = []

    def __init__(self):
        try:
            self.__path_read = config.path_order
        except Exception as e:
            pass

    def load_data(self):
        try:
            if self.__path_read == '':
                return
            log_show(msg='buscando ficheros', level='info', procedure='load_data', file=__class__)

            list = get_files(path=self.__path_read, extension='in')
            log_show(msg=f'it find {len(list)} file', level='info', procedure='load_data', file=__class__)

            global status
            global is_error

            for name_file in list:
                status = False
                is_error = False
                name_path = f'{self.__path_read}//{name_file}'
                file_size = os.path.getsize(name_path)

                if file_size <= 0:
                    return

                if os.path.exists(name_path):
                    with open(name_path, encoding="utf-8") as file:
                        try:
                            content = file.read().strip('').replace('\ufeff', '')
                            print('contenido:', content[0:50])
                            if content == '':
                                log_show(msg='error fichero vacio', level='info', procedure='load_data', file=__class__)
                                is_error = True
                                # os.renames(name_path, f'{name_path}.error')
                                status = False
                                return

                            if not content.strip().startswith('MSH|'):
                                log_show(msg='archivo no es un hl7', level='info', procedure='load_data',
                                         file=__class__)
                                is_error = True
                                # os.renames(name_path, f'{name_path}.error')
                                status = False
                                return

                            client = ClientSocket()
                            log_show(msg='enviando mensaje', level='info', procedure='load_data', file=__class__)
                            status = client.send_data(content)
                        except Exception as e:
                            log_show(msg=e, level='error', procedure='load_data', file=__class__)
                        finally:
                            file.close()

                    print('is_error: ', is_error)
                    if is_error:
                        os.renames(name_path, f'{name_path}.error')
                        status = False
                    else:
                        if status:
                            # os.unlink(name_path)
                            os.renames(name_path, f'{name_path}.procesado')
                            log_show(msg='fichero borrado', level='info', procedure='load_data', file=__class__)
                        else:
                            os.renames(name_path, f'{name_path}.error')
                            log_show(msg='sin respuesta del server ', level='info', procedure='load_data',
                                     file=__class__)
        except Exception as e:
            log_show(msg=e, level='error', procedure='load_data', file=__class__)

    def get_path_read(self) -> str:
        return self.__path_read

    def get_list_file(self) -> []:
        return self.__list

    path_read = property(fget=get_path_read)
    list_file = property(fget=get_list_file)


if __name__ == '__main__':
    loadHL7 = ReadHL7()
    while True:
        time.sleep(1)
        loadHL7.load_data()
        time.sleep(5)
