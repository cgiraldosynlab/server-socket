import datetime
import os
import time
import gc
from models.data_sqlite import LogApp
from config.db import Database, SQLite
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client

from config import Config
from helpers import get_fecha, clearConsole

cnf = Config()

class SynlabSOAP:

    __DB__ = None
    __is_test = False

    def __init__(self):
        if cnf.global_enviroment.get('PYTHON_ENV'):
            if cnf.global_enviroment['PYTHON_ENV'] == 'production':
                self.URL_SOAP = cnf.global_enviroment['WSDL_PROD']
            elif cnf.global_enviroment['PYTHON_ENV'] == 'develop':
                self.__is_test = True
                self.URL_SOAP = cnf.global_enviroment['WSDL_TEST']
            else:
                self.URL_SOAP = 'http://container.angel.com.co:8091/WSDLLInterconexiones.dll/wsdl/IIntegracion'
        else:
            self.URL_SOAP = 'http://container.angel.com.co:8091/WSDLLInterconexiones.dll/wsdl/IIntegracion'

        self.USERNAME = 'HIUSJ'
        self.PASSWORD = 'SElVU0o='
        self.__DB__ = SQLite()
        self.__PG__ = Database()

        if self.__is_test:
            try:
                sql_search = "select pid from pg_catalog.pg_stat_activity where datname = %s and application_name IN %s"
                sql_update_pg = 'select pg_terminate_backend(%s)'
                rows = self.__PG__.query(sql_search, ('WINSISLAB_AVENIDA', ('WEBSERVICES', 'WEBSERVICES-LOG')))
                if rows:
                    for row in rows:
                        self.__PG__.query(sql_update_pg, (row.pid,))
            except Exception as e:
                print(e)

    def send_order(self, id_queue, content, control_id):
        try:
            print(f'[x] {fecha} | WSDL | enviando id_queue | {id_queue}')
            imp = Import('http://schemas.xmlsoap.org/soap/encoding/') #, location='http://schemas.xmlsoap.org/soap/encoding/')
            doctor = ImportDoctor(imp)
            client = Client(self.URL_SOAP, doctor=doctor)

            ''' autenticación '''
            request_auth = client.factory.create('ns2:TclAutheticate')
            request_auth.Username = self.USERNAME
            request_auth.Password = self.PASSWORD

            ''' message in HL7 '''
            request_data = client.factory.create('ns2:TclMessageHL7')
            request_data.ControlID = id_queue if control_id == '' else control_id
            request_data.Version = '2.3'
            request_data.TypeMessage = 'ORM^0O1'
            request_data.MessageHL7 = content

            response = client.service.SetMessageHL7(request_auth, request_data)
            time.sleep(1)
            if response:
                try:
                    sql_update = "update t013_queues set f013_response = ?, f013_indicted = 1, f013_indicted_at = (select (datetime('now', 'localtime'))) where f013_id = ?"
                    self.__DB__.cursor.execute(sql_update, (str(response.MessageHL7), id_queue))
                    self.__DB__.conn.commit()
                except Exception as e:
                    self.__DB__.conn.rollback()
                    LogApp(mensaje=f'error al marcar el registro como guardado \n error: {e}')

                ''' finally conections the services web'''
                try:
                    sql_search = "select pid from pg_catalog.pg_stat_activity where datname = %s and application_name in %s"
                    sql_update_pg = 'select pg_terminate_backend( %s )'
                    rows = self.__PG__.conn(sql_search, ('WINSISLAB_AVENIDA', ('WEBSERVICES', 'WEBSERVICES-LOG')))
                    if rows:
                        for row in rows:
                            self.__PG__.query(sql_update_pg, (row.pid, ))
                except:
                    pass

                time.sleep(1)
        except Exception as e:
            LogApp(mensaje=f'error al enviar el fichero HL7 \n error: {e}')

class OrderHL7(Database, SQLite):

    __SQL = '''
            SELECT DISTINCT 
                   o.f008_id
                 , o.f008_number
                 , o.f008_date
                 , o.f008_time
                 , replace(o.f008_date,"-","") || 
                   replace(o.f008_time,":","") as FechaHora
                 , tl.f004_code
                 , o.f008_priority
                 , o.f008_type_service
                 , o.f008_service
                 , o.f008_f004_id
                 , o.f008_f006_id
                 , o.f008_bed
                 , o.f008_history
                 , tc.f006_code
                 , tc.f006_name
                 , ttd.f002_code
                 , tp.f003_number
                 , tp.f003_first_name
                 , tp.f003_second_name
                 , tp.f003_last_name
                 , tp.f003_middle_name
                 , tp.f003_birth_date
                 , tp.f003_gender
                 , tp.f003_address
                 , tp.f003_cell_phone
                 , tp.f003_phone
                 , tp.f003_email
                 , tm.f007_control_id
              FROM t008_orders  		o
        INNER JOIN t007_messages        tm  ON (tm.f007_id      = o.f008_f007_id )
        INNER JOIN t009_details 		od  ON (od.f009_f008_id = o.f008_id      )
        INNER JOIN t012_test    		tt  ON (tt.f012_code    = od.f009_test   )
        INNER JOIN t003_patients 		tp  ON (tp.f003_id      = o.f008_f003_id )
        INNER JOIN t002_types_documents ttd ON (ttd.f002_id     = tp.f003_f002_id)
        INNER JOIN t004_locations       tl  ON (tl.f004_id      = o.f008_f004_id )
        INNER JOIN t006_companies       tc  ON (tc.f006_id      = o.f008_f006_id )
             WHERE od.f009_indicted = False
               AND tt.f012_group_by = ?
          ORDER BY o.f008_id ASC '''

    __SQLDETAILS = '''
            SELECT od.f009_id
                 , od.f009_barcode
                 , od.f009_sequence
                 , od.f009_test
                 , od.f009_name
                 , od.f009_date_test
                 , replace(replace(replace(od.f009_date_test, "-",""), ":", ""), " ", "") as FechaHora
              FROM t008_orders  		o
        INNER JOIN t009_details 		od  ON (od.f009_f008_id = o.f008_id)
        INNER JOIN t012_test    		tt  ON (tt.f012_code    = od.f009_test)
             WHERE od.f009_indicted = False
               AND tt.f012_group_by = ?
               AND od.f009_f008_id  = ?
          ORDER BY o.f008_id ASC '''

    def __init__(self):
        super().__init__()
        try:
            self.db = SQLite()
        except Exception as e:
            pass

    def search(self):
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[x] {fecha} | SEARCH | buscando examenes tipo 0')

            rows = self.db.cursor.execute(self.__SQL, (0, )).fetchall()
            index = 0
            for row in rows:
                format = '%Y%m%d%H%M%S'
                service_cod = ''

                if str(row['f008_type_service']).upper() == 'P':
                    service_cod = f"PARTICULAR-{row['f004_code']}"
                else:
                    service_cod = row["f008_service"]

                hl7_geral = f'MSH|^~\&|HIUSJ||SYNLABCOL||{datetime.datetime.now().strftime("%Y%m%d%H%M")}||ORM^O01|{row["f007_control_id"]}|P|2.3||||||8859/1||||||||| \n'
                hl7_geral += f'PID|1|{row["f002_code"]}^{row["f003_number"]}|{row["f008_history"]}|{row["f008_history"]}|{row["f003_last_name"]} {row["f003_middle_name"]}^{row["f003_first_name"]} {row["f003_second_name"]}||{str(row["f003_birth_date"]).replace("-", "")}|{row["f003_gender"]}|||sin datos||0|{row["f003_email"]}||||||||||||||||||||||||||| \n'
                hl7_geral += f'PV1|1|{row["f008_type_service"]}^{row["f008_bed"]}|||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'IN1|1|860030582|443^Hospital Infantil Universitario de San Jose||||||||||||||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'ORC|NW|{row["f008_number"]}^860030582||||||{row["FechaHora"]}|{row["FechaHora"]}|0|||||{service_cod}^{row["f006_name"]}^^{row["f006_code"]}^{row["f006_name"]}|||||||||||||||||||| \n'

                ''' buscar detalles de la orden '''
                obr_pos = 1
                rows_details = self.db.cursor.execute(self.__SQLDETAILS, (0, row['f008_id'])).fetchall()
                for item in rows_details:
                    hl7_geral += f'OBR|{obr_pos}|{item["f009_barcode"]}^860030582||{item["f009_test"]}^{item["f009_name"]}|||||{item["FechaHora"]}|||||||||||||||||||||||||||||||||||||||||||||| \n'
                    try:
                        self.db.cursor.execute(
                            'UPDATE t009_details SET f009_indicted = TRUE, f009_indicted_at = (SELECT (datetime("now", "localtime"))) WHERE f009_id = ?',
                            (item['f009_id'],))
                        self.db.conn.commit()
                    except Exception as e:
                        self.db.conn.rollback()
                        print(e)
                    obr_pos += 1

                ''' guardar mensaje '''
                try:
                    self.db.cursor.execute("insert into t013_queues (f013_f008_id, f013_control_id, f013_content ) values ( ?, ?, ? )", (row['f008_id'], row['f008_id'], hl7_geral))
                    self.db.conn.commit()
                    if self.db.cursor.rowcount > 0:
                        synlabSoap = SynlabSOAP()
                        synlabSoap.send_order(self.db.cursor.lastrowid, hl7_geral, row["f007_control_id"])
                except Exception as e:
                    print(f'[x] {fecha} | ERROR-HL7 | error al guardar el fichero HL7 | {e}')
                    self.db.conn.rollback()

                index += 1
            else:
                fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'[x] {fecha} | SEARCH-END | fin de la generación de ficheros HL7')
        except Exception as e:
            print(f'[x] {fecha} | ERROR | error al buscar los examenes | {e}')

    def search_covid(self):
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[x] {fecha} | SEARCH | buscando examenes tipo 1')

            rows = self.db.cursor.execute(self.__SQL, (1, )).fetchall()
            index = 0
            for row in rows:
                format = '%Y%m%d%H%M%S'
                service_cod = f'{row["f008_service"]}-COVID'

                if str(row['f008_type_service']).upper() == 'P':
                    service_cod = f"PARTICULAR-{row['f004_code']}-COVID"
                else:
                    service_cod = f'{row["f008_service"]}-COVID'

                hl7_geral = f'MSH|^~\&|HIUSJ||SYNLABCOL||{datetime.datetime.now().strftime("%Y%m%d%H%M")}||ORM^O01|{row["f007_control_id"]}|P|2.3||||||8859/1||||||||| \n'
                hl7_geral += f'PID|1|{row["f002_code"]}^{row["f003_number"]}|{row["f008_history"]}|{row["f008_history"]}|{row["f003_last_name"]} {row["f003_middle_name"]}^{row["f003_first_name"]} {row["f003_second_name"]}||{str(row["f003_birth_date"]).replace("-","")}|{row["f003_gender"]}|||sin datos||0|{row["f003_email"]}||||||||||||||||||||||||||| \n'
                hl7_geral += f'PV1|1|{row["f008_type_service"]}|{row["f008_bed"]}||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'IN1|1|860030582|443^Hospital Infantil Universitario de San Jose||||||||||||||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'ORC|NW|{row["f008_number"]}-COVID^860030582||||||{row["FechaHora"]}|{row["FechaHora"]}|0|||||{service_cod}^{row["f006_name"]}^^{row["f006_code"]}^{row["f006_name"]}|||||||||||||||||||| \n'

                ''' buscar detalles de la orden '''
                obr_pos = 1
                rows_details = self.db.cursor.execute(self.__SQLDETAILS, (1, row['f008_id'], ))
                for item in rows_details:
                    hl7_geral += f'OBR|{obr_pos}|{item["f009_barcode"]}^860030582||{item["f009_test"]}^{item["f009_name"]}|||||{item["FechaHora"]}|||||||||||||||||||||||||||||||||||||||||||||| \n'
                    try:
                        self.db.cursor.execute('UPDATE t009_details SET f009_indicted = TRUE, f009_indicted_at = (SELECT (datetime("now", "localtime"))) WHERE f009_id = ?', (item['f009_id'], ))
                        self.db.conn.commit()
                        if self.db.cursor.rowcount > 0:
                            synlabSoap = SynlabSOAP()
                            synlabSoap.send_order(self.db.cursor.lastrowid, hl7_geral, row["f007_control_id"])
                    except Exception as e:
                        self.db.conn.rollback()
                        print(e)
                    obr_pos += 1

                ''' guardar mensaje '''
                try:
                    self.db.cursor.execute("insert into t013_queues (f013_f008_id, f013_control_id, f013_content ) values ( ?, ?, ? )", (row['f008_id'], row['f007_control_id'], hl7_geral))
                    self.db.conn.commit()
                except Exception as e:
                    print(f'[x] {fecha} | ERROR-HL7 | error al guardar el fichero HL7 | {e}')
                    self.db.conn.rollback()

                index += 1
            else:
                fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'[x] {fecha} | SEARCH-END | fin de la generación de ficheros HL7')
        except Exception as e:
            print(f'[x] {fecha} | ERROR-COVID | error al buscar los examenes | {e}')

    def send_pend(self):
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[x] {fecha} | PEND | buscando información pendiente para enviar')

            rows = self.db.cursor.execute("""SELECT tq.f013_id, tq.f013_content
                                               FROM t013_queues tq
                                              WHERE tq.f013_indicted = False
                                           ORDER BY f013_id ASC""").fetchall()
            if rows:
                for row in rows:
                    print(f"[x] {fecha} | WSDL | enviando id_queue | {row['f013_id']}")
                    synlabSoap = SynlabSOAP()
                    synlabSoap.send_order(row['f013_id'], row['f013_content'], ro)
        except Exception as e:
            pass


print(f'[+] {get_fecha()} | BEGIN | iniciando integración ')
fecha = get_fecha()
order = OrderHL7()
try:
    borrar = 0
    while True:
        ''' buscar todas las ordenes pendientes por trasmitir '''
        try:
            time.sleep(1)
            order.search()
            time.sleep(1)
            order.search_covid()
            time.sleep(1)
            order.send_pend()

            if borrar >= 50:
                borrar = 0
                try:
                    clearConsole()
                except:
                    pass
        except Exception as e:
            print(f'[x] {fecha} | ERROR | error al buscar la data | error: {e} ')
        finally:
            gc.collect()
finally:
    print(f'[+] {fecha} | FINISHED | finalizando integración ')
    gc.collect()
