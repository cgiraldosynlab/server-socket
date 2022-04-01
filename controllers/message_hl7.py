import uuid
import datetime
from config.db import Database

class MSH:
    field_separator = ''
    encoding_caracteres = '^~\&'
    sender = 'SYNLAB'
    sender_facility = ''
    receptor = ''
    receptor_facility = ''
    date_message = datetime.datetime.now().strftime('%Y%M%D%H%M%S%f').replace('/', '')
    security = ''
    message_type = type
    control_id = uuid.uuid4().hex
    process_id = ''
    version = ''
    sequence_numer = 0
    continuation_pointer = ''

    def __init__(self, type, version, **kwargs):

        try:
            if kwargs.get('trama'):
                msh_str = kwargs.get('trama')
                return
            else:
                self.field_separator = ''
                self.encoding_caracteres = '^~\&'
                self.sender = 'SYNLAB'
                self.sender_facility = ''
                self.receptor = ''
                self.receptor_facility = ''
                self.date_message = datetime.datetime.now().strftime('%Y%M%D%H%M%S%f').replace('/', '')
                self.security = ''
                self.message_type = type
                self.control_id = uuid.uuid1()
                self.process_id = ''
                self.version = version
                self.sequence_numer = 0
                self.continuation_pointer = ''
        except Exception as e:
            print('error ini', e)

    def get_str(self) -> str:
        try:
            msg_str = f'MSH|{self.field_separator}|'
            msg_str += f'{self.encoding_caracteres}|'
            msg_str += f'{self.sender}|'
            msg_str += f'{self.sender_facility}|'
            msg_str += f'{self.receptor}|'
            msg_str += f'{self.receptor_facility}|'
            msg_str += f'{self.date_message}|'
            msg_str += f'{self.security}|'
            msg_str += f'{self.message_type}|'
            msg_str += f'{self.control_id}|'
            msg_str += f'{self.process_id}|'
            msg_str += f'{self.version}\r'
            return msg_str
        except Exception as e:
            return e

class MSA:

    def __init__(self, control_id):
        try:
            self.acknowledgment_code = 1
            self.message_control_id = control_id
            self.message = ''
            self.sequence_number = 0
            self.delayed_Acknowledgment_type = ''
            self.error_condition = ''
            self.message_waiting_number = 0
            self.message_waiting_priority = 'H'
        except Exception as e:
            print('error - msa', e)

    def get_str(self):
        msg_return = f'MSA|{self.acknowledgment_code}|'
        msg_return += f'{self.message_control_id}|'
        msg_return += f'{self.message}|'
        msg_return += f'{self.sequence_number}|'
        msg_return += f'{self.delayed_Acknowledgment_type}|'
        msg_return += f'{self.error_condition}|'
        msg_return += f'{self.message_waiting_number}|'
        msg_return += f'{self.message_waiting_priority}|\r'
        return msg_return

class ACK:

    def __init__(self, version):
        try:
            self.__msh = MSH(type='ack^ack'.upper(), version=version)
            self.__msa = []
        except Exception as e:
            print('ACK-ERROR', e)

    def add_msa(self, msa):
        try:
            self.__msa.append(msa)
        except Exception as e:
            print(e)

    def version(self, version):
        self.__msh.version = version

    def get_str(self) -> str:
        try:
            return self.__msh.get_str() + '\r'.join(self.__msa)
        except Exception as e:
            return e

class PID:
    pass