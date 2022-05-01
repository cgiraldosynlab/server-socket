# proyecto de prueba para conexión con socket
import datetime
import os
import socket
import random
import time

class ClientSocket:

    __MENSAJE = None

    def __init__(self):
        value = ''

        if not os.path.exists('files'):
            os.mkdir('files')

        ruta = f'{os.path.dirname(__file__)}/message.hl7'
        if os.path.exists(ruta):
            value = open(ruta)
            self.__MENSAJE = chr(11) + value.read() + chr(28)
        else:
            value = input('Ingresar un valor a enviar para el servidor: ')

    def enviar(self, msg_custom=None):
        try:
            # conectar con el server
            __CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __CLIENT.settimeout(120)
            __CLIENT.connect((os.environ.get('SOCKET_SERVER_HOST'), int(os.environ.get('SOCKET_SERVER_PORT'))))

            if msg_custom is not None:
                __CLIENT.send(msg_custom.encode())
                resp = __CLIENT.recv(1024)
                if self.__MENSAJE and self.__MENSAJE is not None:
                    if resp:
                        print(f'[x] response: {resp.decode()}')
                    else:
                        print('[x] ERROR: no se obtuvo respuesta del servidor')
                else:
                    print('[x] no hay mensaje para enviar')
            else:
                __CLIENT.send(self.__MENSAJE.encode(encoding='utf-8'))
                resp = __CLIENT.recv(1024)
                if self.__MENSAJE and self.__MENSAJE is not None:
                    if resp:
                        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        #print(f'[x] {fecha} | response: {resp.decode().replace(chr(11), "").replace(chr(28), "")}')
                        print(f'[x] {fecha} | response: {resp.decode()}')
                        try:
                            ruta = os.path.dirname(__file__) + '/files'
                            f = open(f'{ruta}/escribir_{str(random.randrange(0, 100000))}.txt', 'w')
                            f.write(resp.decode())
                            f.close()
                        except:
                            print('error')
                    else:
                        print('[x] ERROR: no se obtuvo respuesta del servidor')
                else:
                    print('[x] no hay mensaje para enviar')
            __CLIENT.close()
        except Exception as e:
            print(e)

    def count_message(self):
        try:
            files = os.listdir('files/pendiente')
            print(len(files))
            files = os.listdir('files')
            print(len(files))
            files = os.listdir('files')
            print(len(files))
        except Exception as e:
            print(e)

    def send_order_database(self):
        try:
            from config.db import Database
            db = Database()
            rows = db.query("""
                select ln_id         as ID
                     , ln_fecha      as FECHA
                     , ln_hora       as HORA
                     , ln_u_usuarios as CODIGO
                     , ln_mensaje    as MENSAJE
                  from log.log_in li
                 where li.ln_fecha        >= %s
                   and li.ln_u_usuarios like %s
            """, ('2022-04-25', 'HISJOB-%'))

            cant_ordenes = len(rows)
            try:
                cant_enviar = int(input(f'Cantidad de ordenes que desea enviar (hay {cant_ordenes} disp para enviar): '))
            except:
                cant_enviar = 1

            if cant_enviar > 0:
                index = 0
                for row in rows:
                    ''' enviar orden al socket '''
                    self.enviar(msg_custom=row.mensaje)
                    time.sleep(1)
                    index += 1

                    if index >= cant_enviar:
                        break
        except Exception as e:
            print(e)

cs = ClientSocket()
cant = 1
try:
    try:
        option = int(input('Desea enviar ordenes realaes o desde el archivo (0: Reals | 1: File | 2: close): '))
    except:
        option = 2

    if option == 1:
        cant = int(input('cuantos mensajes desea enviar: '))
        for item in range(cant):
            cs.enviar()
        else:
            cs.count_message()
    elif option == 0:
        cs.send_order_database()
    elif option == 2:
        cs.enviar(msg_custom='close')
except:
    cant = 1

if option == 1:
    dato = str(input('Deseas borrar el log (S / N): '))
    if dato.lower() == 's':
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((os.environ.get('SOCKET_SERVER_HOST'), int(os.environ.get('SOCKET_SERVER_PORT'))))
        byt = 'delete-logs'.encode() # dato.encode()
        sc.send(byt)
        resp = sc.recv(1024)
        print(str(resp.decode()))
        sc.close()

        salir = int(input('Desea cerrar el servidor (0: No | 1: Si): '))
        if salir == 1:
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.connect((os.environ.get('SOCKET_SERVER_HOST'), int(os.environ.get('SOCKET_SERVER_PORT'))))
            byt = 'close'.encode()  # dato.encode()
            sc.send(byt)
            resp = sc.recv(1024)
            print(str(resp.decode()))
            sc.close()
            print('end..')
    else:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect(('172.31.4.70', 6002))
        byt = 'close'.encode()  # dato.encode()
        sc.send(byt)
        resp = sc.recv(1024)
        print(str(resp.decode()))
        sc.close()
        print('end..')

