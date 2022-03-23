from models.log import LogFile, LogApp

''' ****  iniciar servidor socket ****'''
try:
    '''
    server = Server()
    if not server.isError():
        if server.listen():
            server.open()
    '''

    lFile = LogFile('H', 'M')
    logApp = LogApp(codigo='python', mensaje='test')
except Exception as e:
    print('error al ejecutar el servidor', e)



