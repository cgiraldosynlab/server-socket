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
from models.data_sqlite import Paciente, Ubicacion, Servicio, Empresa, TipoDocumento, MensajeIn, MensajeError, Orden, Test
from hl7 import (Message, Segment, Component, Sequence, Field, Accessor, HL7Exception)

'''
MAC/LINUX
export SOCKET_SERVER_HOST=localhost SOCKET_SERVER_PORT=8000 SOCKET_SERVER_BUFFER=65507 SOCKET_SERVER_LIMIT_CLIENT=10

WINDOWS
set SOCKET_SERVER_HOST=172.31.5.70
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
        print(f'[x] - {fecha} | INFO | servidor iniciado | {self.__HOST}:{self.__PORT} ')
        while True:

            try:
                resp = ''
                is_response = False
                fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # obtener información del cliente
                (client, addr) = self.__SC.accept()
                __client_str = f'{addr[0]:{addr[1]}}'

                try:
                    # client.setblocking(False)
                    pass
                except:
                    pass

                print(f'[x] - {fecha} | CONNECT | cliente conectado | info: {addr[0]}:{addr[1]}')

                # recibir mensaje
                data = client.recv(self.__BUFFER_MAX)
                if not data: 
                    client.send('error - el mensaje no puede ser vacio'.encode())
                else:

                    try:
                        print(f'[x] - {fecha} | INFO | recibiendo mensaje | info: {addr[0]}:{addr[1]}')
                        mensaje = data.decode(encoding='utf-8').replace(self.__CHAR_IN, '').replace(self.__CHAR_OUT, '')
                        if mensaje == 'close':
                            # mensaje que permite detener el servidor de socket
                            self.__CANCEL = True
                            client.send(f'-- data: {data.decode()}'.encode())
                            print(f'[x] - {fecha} | INFO | servidor cerrado ')
                            break
                        elif mensaje == 'delete-logs':
                            # mensaje que permite borrar los logs de la base de datos
                            Database().delete('delete from log.log_app WHERE l_id > %s', (0,))
                            Database().delete('delete from log.log_out where lout_id > %s', (0,))
                            client.send(f'{data.decode()}'.encode())
                        elif mensaje == 'maintenance':
                            pass
                        else:
                            # recibe cualquier mensaje y debe procesar en formato HL7
                            name_file = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '_' + str(random.randrange(0, 100000))
                            file = open(f'files/{self.__FOLDER_PENDIENTE}/{name_file}.hl7', 'a', encoding='utf-8')

                            try:
                                resp = ACK('2.5')
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
                                    print(f'[x] - {fecha} | INFO | procesando mensaje | info: {addr[0]}:{addr[1]}')
                                    ''' load file '''
                                    lines = open(f'files/{self.__FOLDER_PENDIENTE}/{name_file}.hl7', 'r').readlines()
                                    msj = '\r'.join(lines)
                                    h = hl7.parse(lines=msj, encoding='utf-8')

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

                                    ''' extraer información '''
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

                                        details = []
                                        if mensaje.isFound:

                                            ''' main | processing message '''
                                            is_order = False
                                            is_patient = False
                                            for line in msj.split('\r'):
                                                try:
                                                    seg = line.split('|')[0]
                                                    trama = line.split('|')

                                                    if seg == 'MSH':
                                                        ''' information header '''
                                                        sender = trama[2]
                                                        sender_facility = trama[3]
                                                        reception = trama[4]
                                                        reception_facility = trama[5]
                                                        type_message = trama[8]

                                                        dictMessage = {
                                                            "buscar": False,
                                                            "control_id": trama[9],
                                                            "sender": [sender],
                                                            "sender_facility": sender_facility,
                                                            "reception": reception,
                                                            "reception_facility": reception_facility,
                                                            "type": type_message,
                                                            "content": mensaje_in
                                                        }

                                                        '''
                                                        mensaje = MensajeIn(
                                                            buscar=False,
                                                            control_id=trama[9],
                                                            sender=sender,
                                                            sender_facility=sender_facility,
                                                            reception=reception,
                                                            reception_facility=reception_facility,
                                                            type=type_message,
                                                            content=mensaje_in
                                                        )'''

                                                    elif seg == 'PID':
                                                        ''' information patient '''
                                                        document = trama[4]
                                                        if document.find('^') > 0:
                                                            tipo_doc = document.split('^')[1].strip()
                                                            number_id = document.split('^')[0].strip()
                                                        history = trama[3]
                                                        patient_name = trama[5]

                                                        if patient_name.find('^') > 0:
                                                            name = patient_name.split('^')[1]
                                                            last_name = patient_name.split('^')[0]

                                                            # procesar nombre
                                                            if name.find(' ') > 0:
                                                                name_1 = name.split(' ')[0]
                                                                name_2 = name.split(' ')[1]
                                                            else:
                                                                name_1 = name
                                                                name_2 = ''

                                                            # procesar last_name
                                                            if last_name.find(' ') > 0:
                                                                ape_1 = last_name.split(' ')[0]
                                                                ape_2 = last_name.split(' ')[1]
                                                            else:
                                                                ape_1 = last_name
                                                                ape_2 = ''

                                                        birth_date = trama[7]
                                                        if birth_date != '':
                                                            birth_date = birth_date[0:8]
                                                            birth_date = f'{birth_date[0:4]}-{birth_date[4:6]}-{birth_date[6:8]}'

                                                        gender = trama[8]
                                                        address = trama[11]
                                                        cellphone = trama[13]
                                                        phone = cellphone
                                                        email = trama[14]
                                                        if email.find('^'):
                                                            email = email.split('^')[3]
                                                        expedition = datetime.datetime.now().strftime('%Y-%m-%d')

                                                        if not is_patient:
                                                            is_patient = True

                                                            dictTipoDoc = {
                                                                "code": tipo_doc,
                                                                "name": tipo_doc
                                                            }

                                                            typeDocument = TipoDocumento(codigo=tipo_doc)
                                                            if not typeDocument.get_isfound():
                                                                typeDocument.set_name(tipo_doc)
                                                                typeDocument.set_active(True)
                                                                typeDocument.guardar()

                                                            dicPatient = {
                                                                "tipoDoc": dictTipoDoc,
                                                                "numberId": number_id,
                                                                "first_name": name_1,
                                                                "second_name": name_2,
                                                                "last_name": ape_1,
                                                                "middle_name": ape_2,
                                                                "birth_date": birth_date,
                                                                "gender": gender,
                                                                "expedition": expedition,
                                                                "blood_type": '',
                                                                "address": address,
                                                                "phone": phone,
                                                                "cellphone": cellphone,
                                                                "email": '',
                                                                "active": True
                                                            }

                                                            patient = Paciente(typeDocument, number_id)
                                                            if not patient.isFound:
                                                                patient.guardar(
                                                                    typeId=typeDocument.get_id(),
                                                                    numberId=number_id,
                                                                    first_name=name_1,
                                                                    second_name=name_2,
                                                                    last_name=ape_1,
                                                                    middle_name=ape_2,
                                                                    birth_date=birth_date,
                                                                    gender=gender,
                                                                    expedition=expedition,
                                                                    blood_type='',
                                                                    address=address,
                                                                    phone=phone,
                                                                    cellphone=cellphone,
                                                                    email=email.replace('^', ''),
                                                                    active=True
                                                                )

                                                    elif seg == 'PV1':
                                                        ''' information additional patient '''
                                                        assigned_location = trama[3]
                                                        if assigned_location.find('^') > 0:
                                                            location_cod = assigned_location.split('^')[0]
                                                            bed_cod = assigned_location.split('^')[0]
                                                        else:
                                                            location_cod = assigned_location
                                                            bed_cod = ''

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

                                                    elif seg == 'IN1':
                                                        type_company = trama[2]
                                                        company_cod = trama[3]
                                                        company_nom = trama[4]
                                                        entity_cod = trama[8]
                                                        entity_nom = trama[9]

                                                        company = Empresa(str(company_cod))
                                                        if not company.isFound:
                                                            company.name = str(company_nom).upper()
                                                            company.isActive = True
                                                            company.isDelete = False
                                                            company.guardar()

                                                    elif seg == 'ORC':

                                                        ''' information order '''
                                                        order_number = trama[2]
                                                        if len(order_number.split('-')) > 2:
                                                            order_number = order_number.split('-')[0] + '-' +order_number.split('-')[1]

                                                        create_at = trama[7]
                                                        priority = create_at.split('^')[5]
                                                        if len(create_at.split('^')) > 4:
                                                            create_at = create_at.split('^')[3]

                                                        create_by = trama[12]
                                                        #create_id_by = trama[]

                                                        service_order = ''
                                                        if type_company == 'P':
                                                            service_order = f'PARTICULAR-{location_cod}'
                                                        else:
                                                            service_order = f'{company_cod}-{location_cod}'


                                                        if not is_order:
                                                            isOrder = True
                                                            dicOrden = {
                                                                'number': order_number,
                                                                'date': f'{create_at[0:4]}-{create_at[4:6]}-{create_at[6:8]}',
                                                                'time': f'{create_at[8:10]}:{create_at[10:12]}:{create_at[12:14]}',
                                                                'messageId': mensaje.id,
                                                                'patientId': patient.id,
                                                                'locationId': location.id,
                                                                'serviceId': 'NA',
                                                                'companyId': company.id,
                                                                'priority': 0,
                                                                'bed': bed_cod,
                                                                'type': type_company,
                                                                'entity': entity_cod,
                                                                'history': history,
                                                                #'service': f'{company_cod}-{location_cod}'
                                                                'service': service_order
                                                            }

                                                        '''
                                                        order = Orden(
                                                            number=dicOrden.get('number'),
                                                            date=dicOrden.get('date'),
                                                            time=dicOrden.get('time'),
                                                            messageId=dicOrden.get('messageId'),
                                                            patientId=dicOrden.get('patientId'),
                                                            locationId=dicOrden.get('locationId'),
                                                            serviceId=dicOrden.get('serviceId'),
                                                            companyId=dicOrden.get('companyId'),
                                                            priority=dicOrden.get('priority'),
                                                            bed=dicOrden.get('bed'),
                                                            type=dicOrden.get('type'),
                                                            entity=dicOrden.get('entity'),
                                                            history=dicOrden.get('history')
                                                        )'''

                                                    elif seg == 'OBR':
                                                        position = trama[1]
                                                        if position == '':
                                                            position = len(details)+1

                                                        barcode = trama[2]
                                                        test_cod = trama[4].split('^')[0]
                                                        test_nom = trama[4].split('^')[1]
                                                        date_test = trama[6]

                                                        test = Test(test_cod)
                                                        test.guardar(code=test_cod, name=test_nom.upper(), isActive=True, groupBy=0)

                                                        detail = {
                                                            'barcode': barcode,
                                                            'sequence': position,
                                                            'code': test_cod,
                                                            'name': test_nom,
                                                            'date_test': f'{date_test[0:4]}-{date_test[4:6]}-{date_test[6:8]} 00:00:00'
                                                        }
                                                        details.append(detail)
                                                    elif seg == 'DG1':
                                                        pass
                                                    elif seg == 'OBX':
                                                        pass
                                                except Exception as e:
                                                    print(f'[x] - {fecha} | ERROR | mensaje no procesado | {e}')
                                            else:

                                                is_order = False
                                                is_patient = False

                                                ''' after sending message to database '''
                                                if mensaje:

                                                    # registry order
                                                    order = Orden(
                                                        number=dicOrden.get('number'),
                                                        date=dicOrden.get('date'),
                                                        time=dicOrden.get('time'),
                                                        messageId=dicOrden.get('messageId'),
                                                        patientId=dicOrden.get('patientId'),
                                                        locationId=dicOrden.get('locationId'),
                                                        serviceId=dicOrden.get('serviceId'),
                                                        companyId=dicOrden.get('companyId'),
                                                        priority=dicOrden.get('priority'),
                                                        bed=dicOrden.get('bed'),
                                                        type=dicOrden.get('type'),
                                                        entity=dicOrden.get('entity'),
                                                        history=dicOrden.get('history'),
                                                        service=dicOrden.get('service')
                                                    )

                                                    # registry details
                                                    if order.isFound:
                                                        order.add_details(details)
                                                    else:
                                                        ''' guardar el mensaje de error '''
                                                        MensajeError(
                                                            buscar=False,
                                                            control_id=mensaje.control_id,
                                                            sender=mensaje.sender,
                                                            sender_facility=mensaje.sender_facility,
                                                            reception=mensaje.reception,
                                                            reception_facility=mensaje.reception_facility,
                                                            type='ORM^O01',
                                                            content=mensaje.content,
                                                        )

                                            ''' send message to database '''
                                            msa.message = 'mensaje procesado con éxito'
                                            # resp.add_msa(msa.get_str())
                                        else:
                                            ''' rechazar mensaje '''
                                            pass
                                    except Exception as e:
                                        print(f'[x] - {fecha} | ERROR | error: {e}')

                                # procesar mensaje
                                if mensaje:
                                    mensaje.response = f'{resp.to_hl7()} \n {msa.to_str()}'
                                    mensaje.set_response()

                                if mensaje and mensaje.response and str(mensaje.response) != '':
                                    client.send(f'{self.__CHAR_IN} {mensaje.response}{self.__CHAR_OUT}'.encode())
                                else:
                                    client.send(f'{self.__CHAR_IN} {resp.get_str()}\n{msa.to_str}{self.__CHAR_OUT}'.encode())

                                print(f'[x] - {fecha} | SUCCESS | mensaje procesado con exito  | info: {addr[0]}:{addr[1]}')
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
