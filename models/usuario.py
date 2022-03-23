#import os, sys
#p = os.path.abspath('.')
#sys.path.insert(1, p)
from config.db import Database

class Usuario(Database):

    def __init__(self, usuario):
        super().__init__()
        rows = super().query('select * from public.usuarios where usr_codigo = %s', (usuario,), True)
        if rows:
            self.usuario = rows.usr_codigo
            self.clave = rows.clave
            self.isFound = True
        else:
            self.isFound = False

    def generadorPares(self, limite) -> object:
        num = 1
        myList = []
        while num < limite:
            myList.append(num * 2)
            num += 1
        return myList

    def generadorParesYield(self, limite):
        num = 1
        while num < limite:
            yield num * 2
            num += 1

    def devuelveCiudades(self, *args):
        for args in args:
            for subArgs in args:
                yield subArgs

    def __str__(self):
        if self.isFound:
            return f'Usuario: {self.usuario} | clave: {self.clave}'
        else:
            return 'usuario no encontrado'

class UsuarioWS:

    def __init__(self, user):
        try:
            self.is_found = False
            if user is None or user == '':
                print('error: el parametro usuario es obligatorio')
                return
            else:
                rows = []
        except Exception as e:
            print(e)

    def create(self, **kwargs):
        try:
            pass
        except Exception as e:
            print(e)

    def update(self, id, **kwargs):
        try:
            pass
        except Exception as e:
            print(e)
