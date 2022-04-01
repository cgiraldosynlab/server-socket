# servidor socket
import os
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
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            client, addr = sc.accept()

            # capturar mensaje
            data = client.recv(__BUFFER_MAX__)
            print(f'[x] {fecha} | cliente conectado | {addr[0]}:{addr[1]}')

            if data.decode() == 'close':
                break
            else:
                print('mensaje recibido', len(data.decode()))

            client.send('Hola te saludo desde el servidor'.encode())

            try:
                client.shutdown()
                client.close()
            except Exception as e:
                print(e)
        except Exception as e:
            print('error:', e)
    sc.close()
except Exception as e:
    pass

