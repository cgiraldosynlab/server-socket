import os
import socket
import datetime
import time
import random
from config.db import Database
from models.log import LogApp

class SubirResultados(Database):

    __CHAR_IN = chr(11)
    __CHAR_OUT = chr(28)

    def __init__(self):
        try:
            super().__init__()
            self.__HOST = '192.168.61.245'
            self.__PORT = 2222

            if not os.path.exists('files'):
                os.mkdir('files')
        except:
            pass

    def send(self):
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[x] {fecha} | buscando resultados')
            rows = super().query('''
                select resout_id as id
                     , resout_ipserver as ipserver
                     , resout_contenido as mensaje
                  from web_services.resultado_out ro
                 where ro.resout_fecha_in >= CURRENT_DATE-10
                   and ro.resout_usuario_ws = 'HIUSJ'
                   and ro.resout_publicado  = 1
                   and ro.resout_solicitado = 0
                order by 1 desc limit 1
            ''')
            print(f'[x] {fecha} | cantidad de resultados encontrados {len(rows)} ')
            for row in rows:
                try:
                    fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f'[x] {fecha} | preparando mensaje | id: {row.id}')
                    deadline = time.time() + 20.0
                    __CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    __CLIENT.connect((self.__HOST, self.__PORT))

                    print(f'[x] {fecha} | conectando con el servicio socket | {self.__HOST}:{self.__PORT}')
                    mensaje = f'{self.__CHAR_IN}{row.mensaje}{self.__CHAR_OUT}'
                    __CLIENT.settimeout(120)
                    __CLIENT.send(mensaje.encode(encoding='utf-8'))
                    print(f'[x] {fecha} | mensaje enviado al servicio socket | {self.__HOST}:{self.__PORT} | id: {row.id}')
                    resp = __CLIENT.recv()
                    print(f'[x] {fecha} |  | ')
                    if resp:
                        print(f'[x] {fecha} | guardando respuesta | {self.__HOST}:{self.__PORT} | id: {row.id}')
                        super().update(
                            'update web_services.resultado_out set resout_publicado = %s, resout_respuesta = %s where resout_id = %s and resout_ipserver = %s',
                            (1, resp.decode(), row.id, row.ipserver)
                        )
                        try:
                            ruta = os.path.dirname(__file__) + '/files'
                            f = open(f'{ruta}/os{str(random.randrange(0, 100000))}.txt', 'w')
                            f.write(resp.decode())
                            f.close()
                        except:
                            print('error')
                    else:
                        print(f'[x] {fecha} | no hay respuesta del respuesta del servidor | ')
                    __CLIENT.close()
                except Exception as e:
                    print(f'[x] {fecha} | error al enviar el mensaje | error: {e} | {self.__HOST}:{self.__PORT} | id: {row.id}')
                    super().update(
                        'update web_services.resultado_out set resout_publicado = %s, resout_respuesta = %s where resout_id = %s and resout_ipserver = %s',
                        (1, e, row.id, row.ipserver)
                    )
        except Exception as e:
            print(f'[x] {fecha} | error - {e} ')

client = SubirResultados()
client.send()