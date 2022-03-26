from config.db import Database
import hl7
from hl7apy.core import *
from hl7apy.parser import *
from hl7apy.validation import Validator
from models.log import LogIn

class ORM(Database):

    # properties
    __message = None
    __hl7 = None
    __isLoad = False
    __isHL7 = False

    def __init__(self, msg) -> None:
        try:
            super().__init__()
            if msg != '':
                self.__message = msg
                self.__hl7 = parse_message(message=self.__message, force_validation=False, find_groups=False)
                self.__isLoad = True
                self.__isHL7 = hl7.parse_hl7(self.__message)
                LogIn('socket', self.__message)
        except Exception as e:
            print(__file__, ':', e)

    def set_message(self, msg) -> None:
        try:
            return self.__message
        except Exception as e:
            print(__file__, ':', e)

    def get_header(self):
        try:
            if self.__isLoad:
                return self.__hl7.msh
            else:
                return ''
        except Exception as e:
            pass

    def get_paciente(self):
        try:
            pass
        except Exception as e:
            pass

    def get_ubicacion(self):
        pass

    def get_ordenes(self):
        try:
            # procedimiento para retornar todos los ORD del paciente
            #             
            pass
        except Exception as e:
            print(__file__, ':', e)

    def get_detalles(self):
        pass

    def get_notas(self):
        pass

    def get_notas_obx(self):
        pass

class ACK(Database):
    def __init__(self, **args):
        try:
            print(args)
            super().__init__()
            self.ack = Message('ACK_O01')
            print(self.ack.msh.value)
            self.ack.add_segment('MSA')
        except Exception as e:
            print(e)

    def get_ack(self) -> str:
        return self.ack.value
    
    
