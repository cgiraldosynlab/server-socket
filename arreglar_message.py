from config import Database, Config
from helpers import log_show

cnf = Config()

class ReiniciarData(Database):

    def __init__(self):
        try:
            super().__init__()
        except Exception as e:
            log_show(msg=e, level='error', procedure='__init__', file=__file__)

    def organizar(self) -> bool:

        try:
            sql = '''
                  select oh_id             as id
                       , oh_sede_bd        as sede_bd
                       , oh_user_cod       as user
                       , oh_mensaje        as mensaje
                       , ormhl7_control_id as control_id
                    from web_services.orm_hl7_in oh 
                   where oh.oh_fecha   >= CURRENT_DATE-1 
                     and oh.oh_user_cod = %s
                order by oh_id asc
            '''
            params = ('HIUSJ',)


            rows = self.query(sql, params)
            for row in rows:
                for line in row.mensaje.split('\n'):
                    if line.split('|')[0].upper() == 'MSH':
                        control_id = line.split('|')[9]
                        print(control_id,  row.control_id)
                        if control_id != '' and control_id != row.control_id:
                            try:
                                sql_update = 'update web_services.orm_hl7_in set ormhl7_control_id = %s where oh_id = %s and oh_sede_bd = %s'
                                params_update = (control_id, row.id, row.sede_bd)
                                self.update(sql_update, params_update)
                            except Exception as e:
                                log_show(msg=e, level='error', procedure='for_update', file=__file__)
                        break
        except Exception as e:
            log_show(msg=e, level='error', procedure='organizar', file=__file__)

reload = ReiniciarData()
reload.organizar()
exit(1)