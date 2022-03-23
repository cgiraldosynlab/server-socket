# servidor socket
import datetime
import os
import socket

'''
export SOCKET_SERVER_HOST=localhost SOCKET_SERVER_PORT=8000 SOCKET_SERVER_BUFFER=65507 SOCKET_SERVER_LIMIT_CLIENT=10

dos tipos de pacientes.
un unico plan 9418
paciente de red externa (debe llegar con autorización)
paciente de red externa (Cuando viene de hospital adicional autorización debe presentar ordenes medicas)
si viene con varias autorización se debe ingresar por autorización
WINSISLAB
ambas se ingresan para un no. de autorización.
'''

class Server:

    # definir properties
    __IS_ERROR = False
    __HOST = 'localhost'
    __PORT = 8000
    __BUFFER_MAX = 65507
    __CLIENT_LIMIT = 10
    __SC = None

    def __init__(self):
        try:
            self.__IS_ERROR = False
            self.__HOST = os.environ.get('SOCKET_SERVER_HOST')
            self.__PORT = int(os.environ.get('SOCKET_SERVER_PORT'))
            self.__BUFFER_MAX = int(os.environ.get('SOCKET_SERVER_BUFFER'))
            self.__CLIENT_LIMIT = int(os.environ.get('SOCKET_SERVER_LIMIT_CLIENT'))
            self.__SC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__SC.bind((self.__HOST, self.__PORT))
        except Exception as e:
            self.__IS_ERROR = True
            print(f'error al inicializar el server [{e}]')

    def open(self):
        try:
            print('servidor iniciado...')
            while True:
                try:
                    fecha = datetime.datetime.now()

                    # capturar información del cliente
                    client, addr = self.__SC.accept()
                    print(f'--> {fecha} | client: {addr[0]} | port: {str(addr[1])} |')

                    # recibir mensaje
                    message = b''
                    #message = client.recv(self.__BUFFER_MAX)
                    resp = self.procesar_mensaje(client=client, addr=addr)
                    if resp.decode() == 'close':
                        print('Adios..!!')
                        client.send('adios amigo..!!'.encode())
                        self.close()
                        break
                    else:
                        client.send('te saludo desde el servidor'.encode())
                    client.close()
                except Exception as err:
                    print(f'error al procesar el mensaje [{err}]')
            else:
                print('he salido del while')
        except Exception as e:
            pass

    def procesar_mensaje(self, **kwargs):
        try:
            msg = b''
            if kwargs['client']:
                bloqueo = kwargs['client'].getblocking()
                kwargs['client'].setblocking(True)
                try:
                    while True:
                        msg += kwargs['client'].recv(self.__BUFFER_MAX)
                        #print(len(msg), '|', self.__BUFFER_MAX)

                        # salir del bucle si no hay mas datos para leer
                        if len(msg) < self.__BUFFER_MAX:
                            kwargs['client'].setblocking(False)
                            break
                except Exception as e:
                    print(e)
                finally:
                    kwargs['client'].setblocking(bloqueo)
            return msg
        except Exception as e:
            print('error al procesar el mensaje', e)

    def listen(self, limit=None) -> bool:
        try:
            if self.__SC is not None:
                if limit is None:
                    self.__SC.listen(self.__CLIENT_LIMIT)
                else:
                    self.__SC.listen(limit)
                return True
            else:
                return False
        except Exception as e:
            print('error al activar el servidor', '[', e, ']')
            return False

    def close(self):
        try:
            self.__SC.close()
        except Exception as e:
            print('error al cerrar el servidor ', e)

    def isError(self) -> bool:
        return self.__IS_ERROR

'''
try:
    __BUFFER_MAX__ = 65507
    __HOST__ = 'localhost'
    __PORT__ = 8000

    sc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sc.bind((__HOST__, __PORT__))
    sc.listen(10)
    print('servidor esperando..')
    while True:
        try:
            client, addr = sc.accept()
            print('nueva conexión')
            print(addr)

            # capturar mensaje
            data = client.recv(__BUFFER_MAX__)

            if data.decode() == 'close':
                break
            else:
                #print('data:', data.decode())
                print('mensaje recibido', len(data.decode()))

            client.send('Hola te saludo desde el servidor'.encode())
            client.close()
        except Exception as e:
            print('error:', e)
        finally:
            client.close()

    sc.close()
except Exception as e:
    pass
'''