import datetime
from config.db import *

class LogFile:

    def __init__(self, codigo, mensaje):
        try:
            date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            print(date)
            self.__name_file = ''
        except Exception as e:
            pass


class LogApp(Database):

    def __init__(self, codigo, mensaje, usuario=None):
        try:
            super().__init__()
            self.codigo = codigo
            self.mensaje = mensaje
            if usuario is None:
                self.usuario = 'python'

            super().insert(
                '''
                insert into log.log_app (l_codigo, l_mensaje, l_tipo, l_u_usuario)
                values(%s, %s, 1, %s)
                returning l_id
                ''',
                (self.codigo, self.mensaje, self.usuario)
            )
        except Exception as e:
            print(e)

class LogIn(Database):

    def __init__(self, usuario, mensaje):
        try:
            super().__init__()
            self.usuario = usuario
            self.mensaje = mensaje
            super().insert('insert into log.log_in (ln_u_usuarios, ln_mensaej) values (%s, %s)', (self.usuario, self.mensaje))
        except Exception as e:
            print('error al registrar el log de entrada', e)