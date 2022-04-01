# servidor socket
import os
import gc
import datetime
import socket
try:
    __BUFFER_MAX__ = 65507
    __HOST__ = 'localhost'
    __PORT__ = 8000

    sc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sc.bind((__HOST__, __PORT__))
    sc.listen(10)
    print('servidor iniciado..')
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
        except Exception as e:
            print('error:', e)
        finally:
            client.close()

    sc.close()
except Exception as e:
    pass

