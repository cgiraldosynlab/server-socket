# servidor socket
import os
import gc
import datetime
import socket
import hl7
import random
from models.log import (LogIn, LogApp)
from config.db import Database
from helpers.logger import LogSys
from controllers.message_hl7 import MSH, MSA, ACK

'''
MAC/LINUX
export SOCKET_SERVER_HOST=localhost SOCKET_SERVER_PORT=8000 SOCKET_SERVER_BUFFER=65507 SOCKET_SERVER_LIMIT_CLIENT=10

WINDOWS
set SOCKET_SERVER_HOST=localhost SOCKET_SERVER_PORT=8000 SOCKET_SERVER_BUFFER=65507 SOCKET_SERVER_LIMIT_CLIENT=10

dos tipos de pacientes.
un unico plan 9418
paciente de red externa (debe llegar con autorización)
paciente de red externa (Cuando viene de hospital adicional autorización debe presentar ordenes medicas)
si viene con varias autorización se debe ingresar por autorización
WINSISLAB
ambas se ingresan para un no. de autorización.
'''

'''
    def open(self):
        try:
            fecha = datetime.datetime.now()
            print(f'[x] {fecha} | host: {self.__HOST}:{self.__PORT} | servidor iniciado')
            while True:
                try:
                    fecha = datetime.datetime.now()

                    # capturar información del cliente
                    client, addr = self.__SC.accept()
                    try:                        
                        client.setblocking(False)
                        self.__listClient.append(client)
                        print(f'[x] {fecha} | client: {addr[0]}:{addr[1]} ')
                    except:
                        pass

                    # recibir mensaje                    
                    resp = self.procesar_mensaje(client=client, addr=addr)
                    if resp and resp.decode() != '':
                        if resp.decode() == 'close':
                            print(f'[x] {fecha} | client: {addr[0]} | port: {str(addr[1])} | petición de cerrado ejecutandose')
                            client.send('el servidor se cerrara por mantenimiento'.encode())
                            self.close()
                            break
                        elif resp.decode() == 'delete-log':
                            Database().delete('DELETE FROM log.log_app WHERE l_id > %s', (0, ))
                            client.send('log eliminado con éxito'.encode())
                        else:
                            try:
                                LogApp('python', resp.decode())
                                client.send('te saludo desde el servidor'.encode())
                            except Exception as err:
                                LogApp('socket', f'error al procesar el mensaje socket')
                                client.send(f'error - {err}'.encode())                                
                    else: 
                        ack = ACK(control_id=-1, message='el mensaje no puede ser vacio')                        
                        client.send(ack.get_ack().encode())                    
                except Exception as err:
                    print(f'error al procesar el mensaje [{err}]')                    
                finally:
                    if client:
                        client.close()        
        except Exception as e:
            pass

    def procesar_mensaje(self, **kwargs):
        try:
            msg = b''
            if kwargs['client']:
                #bloqueo = kwargs['client'].getblocking()
                bloqueo = False
                #kwargs['client'].setblocking(False)
                while True:
                    try:
                        data = kwargs['client'].recv(self.__BUFFER_MAX)
                        if not data: 
                            msg = b'close'
                            kwargs['client'].setblocking(False)
                            break

                        msg += data                        
                        # salir del bucle si no hay mas datos para leer
                        if len(msg) < self.__BUFFER_MAX:
                            kwargs['client'].setblocking(False)
                            break                    
                    except Exception as e:
                        LogApp('socket', f'1-error al procesar el mensaje - {e}')
                        msg = f'1-error al procesar el mensaje {e}'.encode()
                        break                    
                else: 
                    #kwargs['client'].setblocking(bloqueo)
                    pass
            return msg
        except Exception as e:
            print('error al procesar el mensaje', e)

    '''

class Server:

    # definir properties
    __IS_ERROR = False
    __HOST = 'localhost'
    __PORT = 8000
    __BUFFER_MAX = 65507    
    __CLIENT_LIMIT = 10
    __SC = None
    __CANCEL = False
    __CHAR_IN = chr(11)
    __CHAR_OUT = f'{chr(28)}{chr(13)}'
    __FOLDER_PENDIENTE = 'pendiente'
    __FOLDER_PROCESADO = 'procesado'

    def __init__(self):
        try:
            self.__IS_ERROR = False
            
            if os.environ.get('SOCKET_SERVER_HOST'):
                self.__HOST = os.environ.get('SOCKET_SERVER_HOST')
                self.__PORT = int(os.environ.get('SOCKET_SERVER_PORT'))
                self.__BUFFER_MAX = int(os.environ.get('SOCKET_SERVER_BUFFER'))
                self.__CLIENT_LIMIT = int(os.environ.get('SOCKET_SERVER_LIMIT_CLIENT'))
            else: 
                self.__HOST = 'localhost'
                self.__PORT = 8000
                self.__BUFFER_MAX = 65507
                self.__CLIENT_LIMIT = 10
                
            self.__SC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__SC.bind((self.__HOST, self.__PORT))
        except Exception as e:
            self.__IS_ERROR = True
            LogSys().error('python', f'error inicializando el servicio socket [{e}]')

    def acceptClient(self):

        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[x] - {fecha} | servidor iniciado | {self.__HOST}:{self.__PORT} ')
        while True:

            try:
                resp = ''
                is_response = False
                fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # obtener información del cliente
                (client, addr) = self.__SC.accept()
                __client_str = f'{addr[0]:{addr[1]}}'

                try:
                    pass
                    #client.setblocking(False)
                except:
                    pass

                print(f'[x] - {fecha} | cliente conectado | info: {addr[0]}:{addr[1]}')

                # recibir mensaje
                data = client.recv(self.__BUFFER_MAX)
                if not data: 
                    client.send('error - el mensaje no puede ser vacio'.encode())
                else:

                    try:
                        mensaje = data.decode(encoding='utf-8').replace(self.__CHAR_IN, '').replace(self.__CHAR_OUT, '')
                        if mensaje == 'close':
                            # mensaje que permite detener el servidor de socket
                            self.__CANCEL = True
                            client.send(f'-- data: {data.decode()}'.encode())
                            print(f'[x] - {fecha} | servidor cerrado ')
                            break
                        elif mensaje == 'delete-logs':
                            # mensaje que permite borrar los logs de la base de datos
                            Database().delete('delete from log.log_app WHERE l_id > %s', (0,))
                            Database().delete('delete from log.log_out where lout_id > %s', (0,))
                            client.send(f'{data.decode()}'.encode())
                            pass
                        else:
                            # recibe cualquier mensaje y debe procesar en formato HL7
                            name_file = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '_' + str(random.randrange(0, 100000))
                            file = open(f'files/{self.__FOLDER_PENDIENTE}/{name_file}.hl7', 'a', encoding='utf-8')
                            try:
                                resp = ACK('2.3')
                                msa = MSA('')

                                ''' recepciónar mensaje '''
                                mensaje_in = mensaje
                                LogApp(codigo='python', mensaje=mensaje_in)
                                file.write(mensaje_in)
                                file.close()

                                ''' validar si es un mensaje HL7 '''
                                if not hl7.ishl7(mensaje_in):
                                    msa.message = 'error al formatear el mensaje HL7'
                                    resp.add_msa(msa.get_str())
                                    return

                                ''' load file '''
                                lines = open(f'files/{self.__FOLDER_PENDIENTE}/{name_file}.hl7', 'r').readlines()
                                msj = '\r'.join(lines)
                                h = hl7.parse(lines=msj, encoding='utf-8')

                                ''' procesar mensaje HL7 '''
                                msh = h.segment('MSH')
                                try:
                                    control_id = h['MSH'][0][10]
                                    msa.message_control_id = control_id
                                except Exception as e:
                                    print('control_id:', e)

                                try:
                                    version = h['MSH'][0][12]
                                    resp.version(version)
                                except Exception as e:
                                    print('version:', e)

                                msa.message = 'mensaje procesado con éxito'
                                resp.add_msa(msa.get_str())
                            except Exception as e:
                                # resp = f'error al procesar el mensaje [{e}]'
                                msa = MSA('')
                                msa.message = f'error: {e}'
                                if isinstance(resp, ACK):
                                    resp.add_msa(msa.get_str())

                                if resp is not None:
                                    LogSys().error('socket', f'{resp.get_str()} - error [{e}]')
                            finally:
                                # client.send(f'{self.__CHAR_IN}{resp}{self.__CHAR_OUT}'.encode())
                                if resp is not None and isinstance(resp, ACK):
                                    client.send(f'{self.__CHAR_IN}{resp.get_str()}{self.__CHAR_OUT}'.encode())
                                    is_response = True
                                else:
                                    client.send(f'{self.__CHAR_IN}mensaje no pudo ser decodificado{self.__CHAR_OUT}'.encode())
                                    is_response = True
                    except Exception as e:
                        print('error', e)

            except Exception as e:
                LogSys().error(f'error [{e}]')
                if is_response == False and client is not None:
                    client.send(f'{resp} - error [{e}]'.encode())
            finally:
                if client is not None:
                    client.close()
                gc.collect()

    def listen(self, limit=None) -> bool:
        try:
            LogSys.info('socket', 'socket | method: listen | servidor socket iniciado')
            if self.__SC is not None:
                if limit is None:
                    self.__SC.listen(self.__CLIENT_LIMIT)
                else:
                    self.__SC.listen(limit)
                return True
            else:
                return False
        except Exception as e:
            LogSys().error(f'error al activar el servidor | {e}')
            return False

    def close(self):
        try:
            LogSys().info('socket', 'socket | method: close | servidor socket cerrado')
            self.__SC.close()
        except Exception as e:
            LogSys().error(f'error al cerrar el servidor - error {e}')

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
