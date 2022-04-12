# Ejemplo de instalación de un project

# una vez configurado se ejecuta por consola el python setup.py zdict 
# esto para generar un paraque distribuible
# luego install el paquete con el pip install <nombre del comprimido>

'''
from setuptools import setup, find_packages

def get_readme():
    readme = ''
    try:
        import pypandoc
        readme = pypandoc.convert('README.md', 'rst')
    except (ImportError, IOError):
        with open('README.md', 'r') as file_data:
            readme = file_data.read()
    return readme

setup(
    name='server-socket',
    version='1.0',
    author="Cristian Giraldo",
    author_email='Cristian.Giraldo@synlab.co',
    description=('paquete servidor socket para recepción de ordenes en formato HL7'),
    long_description=get_readme(),
    license='BSD',
    keywords='synlab server socket - hl7',
    url='',
    packages=find_packages(),
    package_data={
        'starwars_ipsum': ['*.txt']
    },
    install_requires=['markdown==2.6.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ]
)'''


'''
    url='',
    packages=[
        "config", 
    ]
'''

# setup, es donde se especifica la descripción del project
# @author: Cristian Giraldo
# @date:

import os
import gc
from config.db import Database, SQLite
from server_socket import Server
from helpers.logger import LogSys
from models.data_sqlite import Usuario, TipoDocumento, Paciente, Ubicacion, Servicio, MensajeIn, Orden

try:
    ruta = f'{os.path.dirname(__file__)}/sql_update.sql'
    if os.path.exists(ruta):
        value = open(ruta)
        lines = value.readlines()
        if len(lines) > 0:
            print('total:', len(lines))
            cant = 0
            database = Database()
            for line in lines:
                if not database.update_sql(line):
                    print(line)
                cant += 1
                print(f'{cant} de {len(lines)}')
    else:
        value = input('ingresar un valor a enviar para el servidor: ')

    # recrear base de datos
    bd_create = SQLite()
except:
    print('error')

try:
    ''' crear directorios '''
    if not os.path.exists('files'):
        os.mkdir('files')
    if not os.path.exists('files/pendiente'):
        os.mkdir('files/pendiente')
    if not os.path.exists('files/procesado'):
        os.mkdir('files/procesado')

    ''' ****  iniciar servidor socket ****'''
    server = Server()
    if not server.isError():
        server.listen()
        server.acceptClient()
except Exception as e:
    print(e)
finally:
    gc.collect()