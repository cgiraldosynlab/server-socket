# Ejemplo de instalación de un project
'''

# una vez configurado se ejecuta por consola el python setup.py zdict 
# esto para generar un paraque distribuible
# luego install el paquete con el pip install <nombre del comprimido>

from setuptools import setup

setup(
    name='serversocket',
    version='1.0',
    description='''''',
    author="Cristian Giraldo",
    author_email='Cristian.Giraldo@synlab.co',
    url='',
    packages=[
        "config", 
    ]
)'''

# setup, es donde se especifica la descripción del project
# @author: Cristian Giraldo
# @date:


from models.log import LogFile, LogApp
from config.db import Database
from server_socket import Server

try:
    ''' ****  iniciar servidor socket ****'''
    server = Server()
    if not server.isError():
        server.listen()
        server.acceptClient()
    '''
    if not server.isError():
        if server.listen():
            server.open()
    '''

    #lFile = LogFile('H', 'M')
    #logApp = LogApp(codigo='python', mensaje='test')
except Exception as e:
    print('error al ejecutar el servidor', e)