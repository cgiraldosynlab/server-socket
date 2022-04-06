# servidor socket
import os
import gc
import datetime
import socket
import hl7
import random
from models.log import (LogIn, LogApp)
from config.db import Database
from helpers.logger import LogSys
from controllers.message_hl7 import MSH, MSA, ACK
from models.data_sqlite import Paciente, Ubicacion, Servicio, Empresa, TipoDocumento, MensajeIn, Orden

'''
MAC/LINUX
export SOCKET_SERVER_HOST=localhost SOCKET_SERVER_PORT=8000 SOCKET_SERVER_BUFFER=65507 SOCKET_SERVER_LIMIT_CLIENT=10

WINDOWS
set SOCKET_SERVER_HOST=localhost 
set SOCKET_SERVER_PORT=8000 
set SOCKET_SERVER_BUFFER=65507 
set SOCKET_SERVER_LIMIT_CLIENT=10

dos tipos de pacientes.
un unico plan 9418
paciente de red externa (debe llegar con autorización)
paciente de red externa (Cuando viene de hospital adicional autorización debe presentar ordenes medicas)
si viene con varias autorización se debe ingresar por autorización
WINSISLAB
ambas se ingresan para un no. de autorización.
'''

'''
    def open(self):
        try:
            fecha = datetime.datetime.now()
            print(f'[x] {fecha} | host: {self.__HOST}:{self.__PORT} | servidor iniciado')
            while True:
                try:
                    fecha = datetime.datetime.now()

                    # capturar información del cliente
                    client, addr = self.__SC.accept()
                    try:                        
                        client.setblocking(False)
                        self.__listClient.append(client)
                        print(f'[x] {fecha} | client: {addr[0]}:{addr[1]} ')
                    except:
                        pass

                    # recibir mensaje                    
                    resp = self.procesar_mensaje(client=client, addr=addr)
                    if resp and resp.decode() != '':
                        if resp.decode() == 'close':
                            print(f'[x] {fecha} | client: {addr[0]} | port: {str(addr[1])} | petición de cerrado ejecutandose')
                            client.send('el servidor se cerrara por mantenimiento'.encode())
                            self.close()
                            break
                        elif resp.decode() == 'delete-log':
                            Database().delete('DELETE FROM log.log_app WHERE l_id > %s', (0, ))
                            client.send('log eliminado con éxito'.encode())
                        else:
                            try:
                                LogApp('python', resp.decode())
                                client.send('te saludo desde el servidor'.encode())
                            except Exception as err:
                                LogApp('socket', f'error al procesar el mensaje socket')
                                client.send(f'error - {err}'.encode())                                
                    else: 
                        ack = ACK(control_id=-1, message='el mensaje no puede ser vacio')                        
                        client.send(ack.get_ack().encode())                    
                except Exception as err:
                    print(f'error al procesar el mensaje [{err}]')                    
                finally:
                    if client:
                        client.close()        
        except Exception as e:
            pass

    def procesar_mensaje(self, **kwargs):
        try:
            msg = b''
            if kwargs['client']:
                #bloqueo = kwargs['client'].getblocking()
                bloqueo = False
                #kwargs['client'].setblocking(False)
                while True:
                    try:
                        data = kwargs['client'].recv(self.__BUFFER_MAX)
                        if not data: 
                            msg = b'close'
                            kwargs['client'].setblocking(False)
                            break

                        msg += data                        
                        # salir del bucle si no hay mas datos para leer
                        if len(msg) < self.__BUFFER_MAX:
                            kwargs['client'].setblocking(False)
                            break                    
                    except Exception as e:
                        LogApp('socket', f'1-error al procesar el mensaje - {e}')
                        msg = f'1-error al procesar el mensaje {e}'.encode()
                        break                    
                else: 
                    #kwargs['client'].setblocking(bloqueo)
                    pass
            return msg
        except Exception as e:
            print('error al procesar el mensaje', e)

    '''

class Server:

    # definir properties
    __IS_ERROR = False
    __HOST = 'localhost'
    __PORT = 8000
    __BUFFER_MAX = 65507    
    __CLIENT_LIMIT = 10
    __SC = None
    __CANCEL = False
    __CHAR_IN = chr(11)
    __CHAR_OUT = f'{chr(28)}{chr(13)}'
    __FOLDER_PENDIENTE = 'pendiente'
    __FOLDER_PROCESADO = 'procesado'

    def __init__(self):
        try:
            self.__IS_ERROR = False
            
            if os.environ.get('SOCKET_SERVER_HOST'):
                self.__HOST = os.environ.get('SOCKET_SERVER_HOST')
                self.__PORT = int(os.environ.get('SOCKET_SERVER_PORT'))
                self.__BUFFER_MAX = int(os.environ.get('SOCKET_SERVER_BUFFER'))
                self.__CLIENT_LIMIT = int(os.environ.get('SOCKET_SERVER_LIMIT_CLIENT'))
            else: 
                self.__HOST = 'localhost'
                self.__PORT = 8000
                self.__BUFFER_MAX = 65507
                self.__CLIENT_LIMIT = 10
                
            self.__SC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__SC.bind((self.__HOST, self.__PORT))
        except Exception as e:
            self.__IS_ERROR = True
            LogSys().error('python', f'error inicializando el servicio socket [{e}]')

    def acceptClient(self):

        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[x] - {fecha} | servidor iniciado | {self.__HOST}:{self.__PORT} ')
        while True:

            try:
                resp = ''
                is_response = False
                fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # obtener información del cliente
                (client, addr) = self.__SC.accept()
                __client_str = f'{addr[0]:{addr[1]}}'

                try:
                    pass
                    #client.setblocking(False)
                except:
                    pass

                print(f'[x] - {fecha} | cliente conectado | info: {addr[0]}:{addr[1]}')

                # recibir mensaje
                data = client.recv(self.__BUFFER_MAX)
                if not data: 
                    client.send('error - el mensaje no puede ser vacio'.encode())
                else:

                    try:
                        mensaje = data.decode(encoding='utf-8').replace(self.__CHAR_IN, '').replace(self.__CHAR_OUT, '')
                        if mensaje == 'close':
                            # mensaje que permite detener el servidor de socket
                            self.__CANCEL = True
                            client.send(f'-- data: {data.decode()}'.encode())
                            print(f'[x] - {fecha} | servidor cerrado ')
                            break
                        elif mensaje == 'delete-logs':
                            # mensaje que permite borrar los logs de la base de datos
                            Database().delete('delete from log.log_app WHERE l_id > %s', (0,))
                            Database().delete('delete from log.log_out where lout_id > %s', (0,))
                            client.send(f'{data.decode()}'.encode())
                        else:
                            # recibe cualquier mensaje y debe procesar en formato HL7
                            name_file = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '_' + str(random.randrange(0, 100000))
                            file = open(f'files/{self.__FOLDER_PENDIENTE}/{name_file}.hl7', 'a', encoding='utf-8')
                            try:
                                resp = ACK('2.3')
                                msa = MSA('')

                                ''' guardar mensaje '''
                                mensaje_in = mensaje
                                LogApp(codigo='python', mensaje=mensaje_in)
                                file.write(mensaje_in)
                                file.close()

                                ''' validar si es un mensaje HL7 '''
                                if not hl7.ishl7(mensaje_in):
                                    msa.message = 'error al formatear el mensaje HL7'
                                    resp.add_msa(msa.get_str())
                                else:
                                    ''' load file '''
                                    lines = open(f'files/{self.__FOLDER_PENDIENTE}/{name_file}.hl7', 'r').readlines()
                                    msj = '\r'.join(lines)
                                    h = hl7.parse(lines=msj, encoding='utf-8')

                                    try:
                                        mensaje = MensajeIn(
                                            buscar=False,
                                            control_id=h['MSH'][0][10][0],
                                            sender=h['MSH'][0][3][0],
                                            sender_facility=h['MSH'][0][4][0],
                                            reception=h['MSH'][0][5][0],
                                            reception_facility=h['MSH'][0][6][0],
                                            type='ORM^O01',
                                            content=mensaje_in,
                                        )

                                        if mensaje.isFound:
                                            ''' processing patient '''
                                            '''
                                            [
                                                [
                                                    ['PID'],            # 0
                                                    ['1'],              # 1
                                                    ['RC1022449020'],   # 2
                                                    ['2050082'],        # 3
                                                    [[['1022449020'], ['RC ']]], # 4
                                                    [[['PULIDO COMAS'], ['ISRAEL ALEJANDRO']]], # 5
                                                    [''],                       # 6
                                                    ['20190527000000'],         # 7
                                                    ['M'],                      # 8
                                                    [[['PULIDO'], ['COMAS']]],  # 9
                                                    [''],                       # 10
                                                    [[['KRA 16 82-95 VEREDA LAS MERCEDES'], [''], ['BOGOTA D.C.'], [''], ['11001']]], # 11
                                                    [''],                       # 12
                                                    ['3144452593'],             # 13
                                                    [[[''], [''], [''], ['Sincorreofe@hospitalinfantildesanjose.org.co']]], # 14
                                                    [''],                       # 15
                                                    ['M\n']                     # 16
                                                ]
                                            ]
                                            '''

                                            dicTipoDoc = {
                                                'codigo': h['PID'][0][4][0][1][0],
                                                'nombre': h['PID'][0][4][0][1][0]
                                            }

                                            typeDoc = TipoDocumento(dicTipoDoc.get('codigo'))
                                            if not typeDoc.get_isfound():
                                                print('entre')
                                                typeDoc.set_name(dicTipoDoc.get('nombre'))
                                                typeDoc.set_active(True)
                                                typeDoc.guardar()

                                            last_name = h['PID'][0][5][0][0]
                                            name_1, name_2 = '', ''
                                            name = h['PID'][0][5][0][1]
                                            ape_1, ape_2 = '', ''

                                            if len(str(last_name).split(' ')) > 1 and len(str(last_name).split(' ')) == 2:
                                                ape_1 = str(last_name).split(' ')[0]
                                                ape_2 = str(last_name).split(' ')[1]
                                            else:
                                                ape_1 = name

                                            if len(str(name).split(' ')) > 1 and len(str(name).split(' ')) == 2:
                                                name_1 = str(name).split(' ')[0]
                                                name_2 = str(name).split(' ')[1]
                                            else:
                                                name_1 = last_name

                                            ''' tratar fechas '''
                                            birth_date = h['PID'][0][7][0]
                                            fecha = f'{birth_date[0:4]}-{birth_date[4:6]}-{birth_date[6:8]}'
                                            birth_date = datetime.datetime.strptime(fecha, '%Y-%m-%d')

                                            dicPatient = {
                                                'typeId': typeDoc.get_id(),
                                                'numberId': h['PID'][0][4][0][0][0],
                                                'first_name': name_1,
                                                'second_name': name_2,
                                                'last_name': ape_1,
                                                'middle_name': ape_2,
                                                'birth_date': birth_date,
                                                'gender': h['PID'][0][8][0][0],
                                                'expedition': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                'blood_type': '',
                                                'address': h['PID'][0][11][0][0][0],
                                                'phone': h['PID'][0][13][0],
                                                'cellphone': h['PID'][0][13][0],
                                                'email': h['PID'][0][14][0][3][0],
                                                'active': True
                                            }
                                            patient = Paciente(typeDoc, dicPatient.get('numberId'))
                                            if not patient.isFound:
                                                patient.guardar(
                                                    typeId=dicPatient.get('typeId'),
                                                    numberId=dicPatient.get('numberId'),
                                                    first_name=dicPatient.get('first_name'),
                                                    second_name=dicPatient.get('second_name'),
                                                    last_name=dicPatient.get('last_name'),
                                                    middle_name=dicPatient.get('middle_name'),
                                                    birth_date=dicPatient.get('birth_date'),
                                                    gender=dicPatient.get('gender'),
                                                    expedition=dicPatient.get('expedition'),
                                                    blood_type=dicPatient.get('blood_type'),
                                                    address=dicPatient.get('address'),
                                                    phone=dicPatient.get('phone'),
                                                    cellphone=dicPatient.get('cellphone'),
                                                    email=dicPatient.get('email'),
                                                    active=True
                                                )

                                            ''' processing segment PV1 '''
                                            '''
                                            [[
                                                ['PV1'],                # 0
                                                ['1'],                  # 1
                                                ['E'],                  # 2
                                                [[['UC04'], ['UP03']]], # 3
                                                [''],           # 4
                                                [''],           # 5
                                                [''],           # 6
                                                [''],           # 7
                                                [''],           # 8
                                                [''],           # 9
                                                [''],           # 10
                                                [''],           # 11
                                                [''],           # 12
                                                [''],           # 13
                                                [''],           # 14
                                                [''],           # 15
                                                [''],           # 16
                                                [''],           # 17
                                                [''],           # 18
                                                ['3591193'],    # 19
                                                ['E'],          # 20
                                            ]]
                                            '''

                                            PV1 = h['PV1'][0]

                                            location_cod = PV1[3][0][0]
                                            bed_cod = PV1[3][0][1][0]

                                            location = Ubicacion(codigo=str(location_cod).strip())
                                            if not location.isFound:
                                                location.name = location_cod
                                                location.isActive = True
                                                location.isDelete = False
                                                location.guardar()

                                            service = Servicio('NA')
                                            if not service.isFound:
                                                service.code = 'NA'
                                                service.name = 'NO APLICA'
                                                service.isActive = True
                                                service.guardar()

                                            ''' processing segment IN1 '''
                                            '''
                                            [[
                                                ['IN1'],                                # 0
                                                ['1'],                                  # 1
                                                ['E'],                                  # 2
                                                ['IPS066'],                             # 3
                                                ['UNION TEMPORAL SERVISALUD SAN JOSE'], # 4
                                                [''],                                   # 5
                                                [''],                                   # 6
                                                [''],                                   # 7
                                                ['02'],                                 # 8
                                                ['INST. PRESTADORAS DE SALUD IPS\n']    # 9
                                            ]]
                                            '''
                                            IN1 = h['IN1']
                                            type_pac = IN1[0][2][0]
                                            company_cod = IN1[0][3]
                                            company_nom = IN1[0][4]
                                            entity_code = IN1[0][8][0]
                                            entity_nom = IN1[0][9]

                                            company = Empresa(str(company_cod))
                                            if not company.isFound:
                                                company.name = str(company_nom).upper()
                                                company.isActive = True
                                                company.isDelete = False
                                                company.guardar()

                                            #print(type_pac, company_cod, company_nom, entity_code, entity_nom)
                                            ''' processing order'''
                                            '''
                                            [
                                                [
                                                    ['ORC'],                # 0
                                                    ['NW'],                 # 1
                                                    ['LB-15878727-6'],      # 2
                                                    [''],                   # 3
                                                    ['671354'],             # 4
                                                    ['SC'],                 # 5
                                                    [''],                   # 6
                                                    [[[''], [''], [''], ['20220309201139'], [''], ['3']]], # 7 
                                                    [''],                   # 8
                                                    [''],                   # 9
                                                    [''],                   # 10
                                                    [''],                   # 11
                                                    [[['hectoro'], ['ORTIZ SANDOVAL'], ['HECTOR EDUARDO'], [''], [''], [''], [''], [''], [''], [''], ['13926430'], [''], ['56'], [''], ['CC13926430\n']]]
                                                ]
                                            ]
                                            '''

                                            # ORC|NW|LB-15878727-6||671354|SC||^^^20220309201139^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430
                                            ORC = h['ORC'][0]
                                            order_number = ORC[2][0]
                                            order_number = order_number.split('-')[0] + '-' + order_number.split('-')[1]
                                            #print(f'Orden: {ORC[2]} - MessageId: {ORC[4]} - fecha: {ORC[7]}')

                                            dicOrden = {
                                                'number': order_number,
                                                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                'time': datetime.datetime.now().strftime('%H:%M:%S'),
                                                'messageId': mensaje.id,
                                                'patientId': patient.id,
                                                'locationId': location.id,
                                                'serviceId': 'NA',
                                                'companyId': company.id,
                                                'priority': 0,
                                                'bed': bed_cod,
                                                'type': type_pac,
                                                'entity': entity_code
                                            }
                                            order = Orden(
                                                number=dicOrden.get('number'),
                                                date=dicOrden.get('date'),
                                                time=dicOrden.get('date'),
                                                messageId=dicOrden.get('time'),
                                                patientId=dicOrden.get('patientId'),
                                                locationId=dicOrden.get('locationId'),
                                                serviceId=dicOrden.get('serviceId'),
                                                companyId=dicOrden.get('companyId'),
                                                priority=dicOrden.get('priority'),
                                                bed=dicOrden.get('bed'),
                                                type=dicOrden.get('type'),
                                                entity=dicOrden.get('entity')
                                            )

                                            ''' processing test '''
                                    except Exception as e:
                                        print(f'[x] - {fecha} | ERROR | error: {e}')

                                    ''' procesar mensaje HL7 '''
                                    try:
                                        control_id = h['MSH'][0][10]
                                        msa.message_control_id = control_id
                                    except Exception as e:
                                        print('control_id:', e)

                                    try:
                                        version = h['MSH'][0][12]
                                        resp.version(version)
                                    except Exception as e:
                                        print('version:', e)

                                    msa.message = 'mensaje procesado con éxito'
                                    resp.add_msa(msa.get_str())

                                    if mensaje:
                                        mensaje.response = resp.get_str()
                                        mensaje.set_response()

                                client.send(f'{self.__CHAR_IN}{resp.get_str()}{self.__CHAR_OUT}'.encode())
                                #client.send(f'{self.__CHAR_IN}{mensaje.response}{self.__CHAR_OUT}'.encode())
                                try:
                                    client.close()
                                except:
                                    pass
                            except Exception as e:
                                print(f'[x] {fecha} | ERROR | error: {e} ')
                                msa = MSA('')
                                msa.message = f'error: {e}'
                                if isinstance(resp, ACK):
                                    resp.add_msa(msa.get_str())
                                if resp is not None:
                                    LogSys().error('socket', f'{resp.get_str()} - error [{e}]')
                    except Exception as e:
                        print('error', e)

            except Exception as e:
                LogSys().error(f'error [{e}]')
            finally:
                gc.collect()

    def listen(self, limit=None) -> bool:
        try:
            LogSys.info('socket', 'socket | method: listen | servidor socket iniciado')
            if self.__SC is not None:
                if limit is None:
                    self.__SC.listen(self.__CLIENT_LIMIT)
                else:
                    self.__SC.listen(limit)
                return True
            else:
                return False
        except Exception as e:
            LogSys().error(f'error al activar el servidor | {e}')
            return False

    def close(self):
        try:
            LogSys().info('socket', 'socket | method: close | servidor socket cerrado')
            self.__SC.close()
        except Exception as e:
            LogSys().error(f'error al cerrar el servidor - error {e}')

    def isError(self) -> bool:
        return self.__IS_ERROR

'''
try:
    __BUFFER_MAX__ = 65507
    __HOST__ = 'localhost'
    __PORT__ = 8000

    sc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sc.bind((__HOST__, __PORT__))
    sc.listen(10)
    print('servidor esperando..')
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
            client.close()
        except Exception as e:
            print('error:', e)
        finally:
            client.close()

    sc.close()
except Exception as e:
    pass
'''
