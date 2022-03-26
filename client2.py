import socket
import time
from hl7 import parse_hl7
from hl7apy.core import *
from hl7apy.parser import *

dato = str(input('Mensaje a enviar: '))
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect(('localhost', 8000))
byt = dato.encode()
sc.send(byt)
resp = sc.recv(1024)
print(str(resp.decode()))
sc.close()