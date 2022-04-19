# SERVER SOCKET - ORDERNES
***
Servidor socket para recepción de ordenes en formato [HL7](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=185). 
El mensaje es recepcionado por el servidor y almacenado en su propia base de datos ([SQLite](https://www.sqlite.org/index.html)),
posteriormente hay un proceso interno que lee las ordenes, las convierte en HL7 Ver. 2.3 y las envia al servicio web de [SYNLAB](https://www.synlab.co).   

## Pre-Requisitos
***
1. [Python](https://www.python.org/)
2. [ODBC Postgres](https://www.postgresql.org/)
3. [Git](https://git-scm.com/)
4. Sistemas operativo Windows 10+ / Windows Server / Linux / MacOS


## Instalacción y configuración
***
1. Descargar aplicación
```
$ git clone https://github.com/cgiraldosynlab/server-socket.git
$ cd server-socket
$ python install requirements.txt 
```

### Configuración de variables de entorno

##### Configuración del servidor

En el sistema operativo se deben crear las siguientes variables de entorno para configuración del servidor socket

| Nombre de la variable       | Descripción                                                    |
|-----------------------------|----------------------------------------------------------------|
| SOCKET_SERVER_HOST          | Dirección del servidor por defecto `Localhost`                 |
| SOCKET_SERVER_PORT          | Puerto de escucha del servidor                                 |
| SOCKET_SERVER_BUFFER        | Tamaño de los mensajes soportados ```min: 1024 / max: 65507``` |
| SOCKET_SERVER_LIMIT_CLIENT  | Cantidad de conexiones soportadas en simultanea.               |

En sistemas operativos Linux/MacOS
```
$ export SOCKET_SERVER_HOST=localhost 
$ export SOCKET_SERVER_PORT=8000 
$ export SOCKET_SERVER_BUFFER=65507 
$ export SOCKET_SERVER_LIMIT_CLIENT=10
```

o se puede ejecutar en una sola linea 
```
$ export SOCKET_SERVER_HOST=localhost SOCKET_SERVER_PORT=8000 SOCKET_SERVER_BUFFER=65507 SOCKET_SERVER_LIMIT_CLIENT=10
```

2. En sistemas operativos Windows
```
$ set SOCKET_SERVER_HOST=localhost
$ set SOCKET_SERVER_PORT=6001
$ set SOCKET_SERVER_BUFFER=65507 
$ set SOCKET_SERVER_LIMIT_CLIENT=10
```

##### Configuración de la conexión a la base de datos.

En el sistema operativo se deben crear las siguientes variable de entorno para conexión a la base de datos.

| Nombre de la variable | Descripción                                             |
|-----------------------|---------------------------------------------------------|
| PG_HOST               | Dirección o IP del servidor de base de datos principal  |
| PG_PORT               | Puerto de comunicación con el servidor de base de datos |
| PG_USERNAME           | Usuario de base de datos                                |
| PG_PASSWORD           | Clave de base de datos                                  |
| PG_DATABASE           | Nombre de la base de datos                              |
| PG_ENCODING           | Tipo de codificación de la base de datos                |

En sistemas operativos Linux/MacOS
```
$ export PG_HOST=localhost 
$ export PG_PORT=5432
$ export PG_USERNAME=demo 
$ export PG_PASSWORD=demo
$ export PG_DATABASE=demo
$ export PG_ENCODING=LATIN1
```
o se puede ejecutar en una sola linea
```
$ export PG_HOST=localhost PG_PORT=5432 PG_USERNAME=demo PG_PASSWORD=demo PG_DATABASE=demo PG_ENCODING=LATIN1
```

En sistemas operativos Windows
```
$ set SOCKET_SERVER_HOST=
$ set SOCKET_SERVER_PORT= 
$ set SOCKET_SERVER_BUFFER= 
$ set SOCKET_SERVER_LIMIT_CLIENT=
```

## Ejecutar servidor
***
1. Abrir la terminal (Linux, MacOS) o la consola cmd (Windows)
2. Ingresar al PATH en donde se encuentra el aplicativo
3. Ejecutar el siguiente comando `$ python setup.py`

> **Importante:** 
> 1. Habilitar el puerto en el Firewall
> 2. Al lanzar el servidor en la ruta `./config` se debe crear un archivo con extensión `.db`

## Ejecutar proceso generación de HL7 2.3
***
1. Abrir la terminal (Linux, MacOS) o la consola cmd (Windows)
2. Ingresar el PATH en donde se encuentra el aplicativo
3. Ejecutar el siguiente comando `$ python hl7_send.py`