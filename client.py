import socket
import time

dato = str(input('Ingresar comando a ejecutar: '))

stMessage = 'MSH|^~\|FACTUG|HISJOB|LIS|LIS|20220310025251||ORM^O01|671354|P|2.5||||||8859/1'
stMessage += 'PID|1|RC1022449020|2050082|1022449020^RC |PULIDO COMAS^ISRAEL ALEJANDRO||20190527000000|M|PULIDO^COMAS||KRA 16 82-95 VEREDA LAS MERCEDES^^BOGOTA D.C.^^11001||3144452593|^^^Sincorreofe@hospitalinfantildesanjose.org.co||M\n'
stMessage += 'PV1|1|E|UC04^UP03||||||||||||||||3591193|E||||||||||||||||||||||||20220204223000\n'
stMessage += 'IN1|1|E|IPS066|UNION TEMPORAL SERVISALUD SAN JOSE||||02|INST. PRESTADORAS DE SALUD IPS\n'
stMessage += 'ORC|NW|LB-15878727-6||671354|SC||^^^20220309201139^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-6||903866^TRANSAMINASA GLUTAMICO PIRUVICA O ALANINO AMINO TRANSFERASA||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-7||671354|SC||^^^20220309201140^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-7||903867^TRANSAMINASA GLUTAMICO OXALACETICA O ASPARTATO AMINO TRANSFE||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-16||671354|SC||^^^20220309201210^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-16||903854^MAGNESIO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-8||671354|SC||^^^20220309201142^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-8||906913^PROTEINA C REACTIVA, CUANTITATIVO DE ALTA PRECISION||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-17||671354|SC||^^^20220309201212^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-17||903604^CALCIO IONICO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-9||671354|SC||^^^20220309201144^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-9||902210^HEMOGRAMA IV (HEMOGLOBINA- HEMATOCRITO- RECUENTO DE ERITROCI||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-10||671354|SC||^^^20220309201146^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-10||902049^TIEMPO DE TROMBOPLASTINA PARCIAL (PTT)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-11||671354|SC||^^^20220309201147^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-11||902045^TIEMPO DE PROTROMBINA (PT)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-12||671354|SC||^^^20220309201205^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-12||903813^CLORO (CLORURO)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-13||671354|SC||^^^20220309201206^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-13||903859^POTASIO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-14||671354|SC||^^^20220309201208^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-14||903864^SODIO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-15||671354|SC||^^^20220309201209^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-15||903835^FOSFORO INORGANICO (FOSFATOS)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-1||671354|SC||^^^20220309201128^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-1||903111^ACIDO LACTICO (L-LACTATO) POR METODO ENZIMATICO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-2||671354|SC||^^^20220309201132^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-2||903809^BILIRRUBINAS TOTAL Y DIRECTA||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-3||671354|SC||^^^20220309201134^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-3||902024^FIBRINOGENO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-4||671354|SC||^^^20220309201136^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-4||903895^CREATININA EN SUERO U OTROS FLUIDOS||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'
stMessage += 'ORC|NW|LB-15878727-5||671354|SC||^^^20220309201137^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\n'
stMessage += 'OBR||LB-15878727-5||903856^NITROGENO UREICO (BUN)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\n'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\n'
stMessage += 'OBX|1|| Peso ||13.00|Kg\n'
stMessage += 'OBX|2||Talla||89.00|Cm\n'

'''
sc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sc.connect(('localhost', 8000))
#message = 'Hola desde el cliente!'
#byt = message.encode()
byt = stMessage.encode()
sc.send(byt)
resp = sc.recv(1024)
print(str(resp.decode()))
sc.close()
'''

for i in range(2):
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = stMessage.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()
    time.sleep(1)

if dato.strip() == 'close':
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = dato.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()
