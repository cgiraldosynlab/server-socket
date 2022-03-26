from models.log import LogFile, LogApp
from config.db import Database
from server_socket import Server

try:    
    Database().delete('DELETE FROM log.log_app WHERE l_id > %s', (0, ))

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