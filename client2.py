# proyecto de prueba para conexión con socket
import datetime
import os
import socket
import random

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
                        print(f'[x] {fecha} | response: {resp.decode().replace(chr(11),"").replace(chr(28),"")}')
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

cs = ClientSocket()

cant = 1
try:
    cant = int(input('cuantos mensajes desea enviar:'))
except:
    cant = 1

https://github.com/cgiraldosynlab/server-socket.git
#cs.enviar('delete-logs')
for item in range(cant):
    cs.enviar()
else:
    cs.count_message()

dato = str(input('Deseas borrar el log (S / N): '))

if dato.lower() == 's':
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = 'delete-logs'.encode() # dato.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()

    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = 'close'.encode()  # dato.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()
    print('end..')
else:
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = 'close'.encode()  # dato.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()
    print('end..')

