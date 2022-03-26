import socket
import time
from hl7 import parse_hl7
from hl7apy.core import *
from hl7apy.parser import *

#dato = str(input('Ingresar comando a ejecutar: '))
dato = 'close_'
if dato.strip() == 'close':
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = dato.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()

stMessage = 'MSH|^~\&|FACTUG|HISJOB|LIS|LIS|20220310025251||ORM^O01|671354|P|2.5||||||8859/1\r'
stMessage += 'PID|1|RC1022449020|2050082|1022449020^RC |PULIDO COMAS^ISRAEL ALEJANDRO||20190527000000|M|PULIDO^COMAS||KRA 16 82-95 VEREDA LAS MERCEDES^^BOGOTA D.C.^^11001||3144452593|^^^Sincorreofe@hospitalinfantildesanjose.org.co||M\r'
stMessage += 'PV1|1|E|UC04^UP03||||||||||||||||3591193|E||||||||||||||||||||||||20220204223000\r'
stMessage += 'IN1|1|E|IPS066|UNION TEMPORAL SERVISALUD SAN JOSE||||02|INST. PRESTADORAS DE SALUD IPS\r'
stMessage += 'ORC|NW|LB-15878727-6||671354|SC||^^^20220309201139^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-6||903866^TRANSAMINASA GLUTAMICO PIRUVICA O ALANINO AMINO TRANSFERASA||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-7||671354|SC||^^^20220309201140^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-7||903867^TRANSAMINASA GLUTAMICO OXALACETICA O ASPARTATO AMINO TRANSFE||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-16||671354|SC||^^^20220309201210^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-16||903854^MAGNESIO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-8||671354|SC||^^^20220309201142^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-8||906913^PROTEINA C REACTIVA, CUANTITATIVO DE ALTA PRECISION||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-17||671354|SC||^^^20220309201212^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-17||903604^CALCIO IONICO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-9||671354|SC||^^^20220309201144^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-9||902210^HEMOGRAMA IV (HEMOGLOBINA- HEMATOCRITO- RECUENTO DE ERITROCI||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-10||671354|SC||^^^20220309201146^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-10||902049^TIEMPO DE TROMBOPLASTINA PARCIAL (PTT)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-11||671354|SC||^^^20220309201147^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-11||902045^TIEMPO DE PROTROMBINA (PT)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-12||671354|SC||^^^20220309201205^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-12||903813^CLORO (CLORURO)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-13||671354|SC||^^^20220309201206^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-13||903859^POTASIO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-14||671354|SC||^^^20220309201208^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-14||903864^SODIO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-15||671354|SC||^^^20220309201209^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-15||903835^FOSFORO INORGANICO (FOSFATOS)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-1||671354|SC||^^^20220309201128^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-1||903111^ACIDO LACTICO (L-LACTATO) POR METODO ENZIMATICO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-2||671354|SC||^^^20220309201132^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-2||903809^BILIRRUBINAS TOTAL Y DIRECTA||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-3||671354|SC||^^^20220309201134^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-3||902024^FIBRINOGENO||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-4||671354|SC||^^^20220309201136^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-4||903895^CREATININA EN SUERO U OTROS FLUIDOS||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'
stMessage += 'ORC|NW|LB-15878727-5||671354|SC||^^^20220309201137^^3|||||hectoro^ORTIZ SANDOVAL^HECTOR EDUARDO^^^^^^^^13926430^^56^^CC13926430\r'
stMessage += 'OBR||LB-15878727-5||903856^NITROGENO UREICO (BUN)||20220309000000|||||||Datos Clinicos||||||||||||||||||^ok\r'
stMessage += 'DG1|1||C910|LEUCEMIA LINFOBLASTICA AGUDA\r'
stMessage += 'OBX|1|| Peso ||13.00|Kg\r'
stMessage += 'OBX|2||Talla||89.00|Cm\r'

hl7_message = stMessage
#h = hl7.parse(message, encoding='latin1')
#print('h[0]:', h[0])

#index = 1
#for segment in h: 
#    print(index, ' >> ', segment)
#    index += 1
'''
detalles = h.segments('OBR')
print(detalles[1])
for det in detalles: 
    print(det[2], '-', det[4][0])
'''

try:    
    m = parse_message(message=stMessage, force_validation=False, find_groups=False, report_file=True)
    #print(m)    
    #print(m.pid)    
    #print(m.msh.sending_application.to_er7())
    #print(m.children)
    msh = m.msh
    print(msh.value)
    print(msh.msh_3.value)
    #print(msh.msh_1)
    #print(msh.msh_2.value)
    #print(msh.msh_3.value)
    #print(msh.msh_4.value)
    #print(msh.msh_5.value)

    '''
    ordens = m.orc
    for orc in ordens: 
        print(orc.value)

    det = m.obr
    for item in det:
        print(item.obr_4.obr_4_1)
    '''
except Exception as e: 
    print(e)

exit(1)
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

for i in range(100):
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = stMessage.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()
    #time.sleep(1)

if dato.strip() == 'close':
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect(('localhost', 8000))
    byt = dato.encode()
    sc.send(byt)
    resp = sc.recv(1024)
    print(str(resp.decode()))
    sc.close()
