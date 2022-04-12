import datetime
import time
import datetime
import gc
from config.db import Database, SQLite

class OrderHL7(Database, SQLite):

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
            sql = '''
                    SELECT DISTINCT 
                           o.f008_id
                         , o.f008_number
                         , o.f008_date
                         , o.f008_time
                         , replace(o.f008_date,"-","") || 
                           replace(o.f008_time,":","") as FechaHora
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
                      FROM t008_orders  		o
                INNER JOIN t009_details 		od  ON (od.f009_f008_id = o.f008_id)
                INNER JOIN t012_test    		tt  ON (tt.f012_code    = od.f009_test)
                INNER JOIN t003_patients 		tp  ON (tp.f003_id      = o.f008_f003_id)
                INNER JOIN t002_types_documents ttd ON (ttd.f002_id     = tp.f003_f002_id)
                INNER JOIN t004_locations       tl  ON (tl.f004_id      = o.f008_f004_id)
                INNER JOIN t006_companies       tc  ON (tc.f006_id      = o.f008_f006_id)
                     WHERE od.f009_indicted = False
                       AND tt.f012_group_by = 0
                  ORDER BY o.f008_id ASC            
            '''

            rows = self.db.cursor.execute(sql).fetchall()
            index = 0
            for row in rows:
                format = '%Y%m%d%H%M%S'
                srevice_cod = ''

                if row['f008_type_service'] == 'P':
                    service_cod = 'PARTICILAR'
                else:
                    service_cod = row["f008_service"]

                hl7_geral = f'MSH|^~\&|HIUSJ||SYNLABCOL||{datetime.datetime.now().strftime("%Y%M%d%H%M%s")}||ORM^O01|{row["f008_id"]}|P|2.3||||||8859/1||||||||| \n'
                hl7_geral += f'PID|1|{row["f002_code"]}^{row["f003_number"]}|{row["f008_history"]}|{row["f008_history"]}|{row["f003_last_name"]} {row["f003_middle_name"]}^{row["f003_first_name"]} {row["f003_second_name"]}||{str(row["f003_birth_date"]).replace("-", "")}|{row["f003_gender"]}|||sin datos||0|{row["f003_email"]}||||||||||||||||||||||||||| \n'
                hl7_geral += f'PV1|1|{row["f008_type_service"]}|{row["f008_bed"]}||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'IN1|1|860030582|443^Hospital Infantil Universitario de San Jose||||||||||||||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'ORC|NW|{row["f008_number"]}^860030582||||||{row["FechaHora"]}|{row["FechaHora"]}|0|||||{service_cod}|||||||||||||||||||| \n'

                ''' buscar detalles de la orden '''
                obr_pos = 1
                sql_det = '''
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
                           AND tt.f012_group_by = 0
                           AND od.f009_f008_id   = ?
                      ORDER BY o.f008_id ASC '''

                rows_details = self.db.cursor.execute(sql_det, (row['f008_id'],)).fetchall()
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
                    self.db.cursor.execute(
                        "insert into t013_queues (f013_f008_id, f013_control_id, f013_content ) values ( ?, ?, ? )",
                        (row['f008_id'], row['f008_id'], hl7_geral))
                    self.db.conn.commit()
                except Exception as e:
                    print(f'[x] {fecha} | ERROR-HL7 | error al guardar el fichero HL7')
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
            #db = SQLite()
            sql = '''
                    SELECT DISTINCT 
                           o.f008_id
                         , o.f008_number
                         , o.f008_date
                         , o.f008_time
                         , replace(o.f008_date,"-","") || 
                           replace(o.f008_time,":","") as FechaHora
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
                      FROM t008_orders  		o
                INNER JOIN t009_details 		od  ON (od.f009_f008_id = o.f008_id)
                INNER JOIN t012_test    		tt  ON (tt.f012_code    = od.f009_test)
                INNER JOIN t003_patients 		tp  ON (tp.f003_id      = o.f008_f003_id)
                INNER JOIN t002_types_documents ttd ON (ttd.f002_id     = tp.f003_f002_id)
                INNER JOIN t004_locations       tl  ON (tl.f004_id      = o.f008_f004_id)
                INNER JOIN t006_companies       tc  ON (tc.f006_id      = o.f008_f006_id)
                     WHERE od.f009_indicted = False
                       AND tt.f012_group_by = 1
                  ORDER BY o.f008_id ASC            
            '''
            rows = self.db.cursor.execute(sql).fetchall()
            index = 0
            for row in rows:
                format = '%Y%m%d%H%M%S'
                srevice_cod = ''

                if row['f008_type_service'] == 'P':
                    service_cod = 'PARTICILAR'
                else:
                    service_cod = row["f008_service"]

                hl7_geral = f'MSH|^~\&|HIUSJ||SYNLABCOL||{datetime.datetime.now().strftime("%Y%M%d%H%M%s")}||ORM^O01|{row["f008_id"]}|P|2.3||||||8859/1||||||||| \n'
                hl7_geral += f'PID|1|{row["f002_code"]}^{row["f003_number"]}|{row["f008_history"]}|{row["f008_history"]}|{row["f003_last_name"]} {row["f003_middle_name"]}^{row["f003_first_name"]} {row["f003_second_name"]}||{str(row["f003_birth_date"]).replace("-","")}|{row["f003_gender"]}|||sin datos||0|{row["f003_email"]}||||||||||||||||||||||||||| \n'
                hl7_geral += f'PV1|1|{row["f008_type_service"]}|{row["f008_bed"]}||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'IN1|1|860030582|443^Hospital Infantil Universitario de San Jose||||||||||||||||||||||||||||||||||||||||||||||||||||| \n'
                hl7_geral += f'ORC|NW|{row["f008_number"]}^860030582||||||{row["FechaHora"]}|{row["FechaHora"]}|0|||||{service_cod}|||||||||||||||||||| \n'

                ''' buscar detalles de la orden '''
                obr_pos = 1
                sql_det = '''
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
                           AND tt.f012_group_by = 1
                           AND od.f009_f008_id  = ?
                      ORDER BY o.f008_id ASC '''

                rows_details = self.db.cursor.execute(sql_det, (row['f008_id'], ))
                for item in rows_details:
                    hl7_geral += f'OBR|{obr_pos}|{item["f009_barcode"]}^860030582||{item["f009_test"]}^{item["f009_name"]}|||||{item["FechaHora"]}|||||||||||||||||||||||||||||||||||||||||||||| \n'
                    try:
                        self.db.cursor.execute('UPDATE t009_details SET f009_indicted = TRUE, f009_indicted_at = (SELECT (datetime("now", "localtime"))) WHERE f009_id = ?', (item['f009_id'], ))
                        self.db.conn.commit()
                    except Exception as e:
                        self.db.conn.rollback()
                        print(e)
                    obr_pos += 1

                ''' guardar mensaje '''
                try:
                    self.db.cursor.execute("insert into t013_queues (f013_f008_id, f013_control_id, f013_content ) values ( ?, ?, ? )", (row['f008_id'], row['f008_id'], hl7_geral))
                    self.db.conn.commit()
                except Exception as e:
                    print(f'[x] {fecha} | ERROR-HL7 | error al guardar el fichero HL7')
                    self.db.conn.rollback()

                index += 1
            else:
                fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'[x] {fecha} | SEARCH-END | fin de la generación de ficheros HL7')
        except Exception as e:
            print(f'[x] {fecha} | ERROR-COVID | error al buscar los examenes | {e}')


fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'[x] {fecha} | BEGIN | iniciando integración ')

order = OrderHL7()
try:
    while True:
        ''' buscar todas las ordenes pendientes por trasmitir '''
        try:
            order.search()
            time.sleep(1)
            order.search_covid()
            time.sleep(1)
        except Exception as e:
            print(f'[x] {fecha} | ERROR | error al buscar la data | error: {e} ')
        finally:
            gc.collect()
finally:
    print(f'[x] {fecha} | FINISHED | finalizando integración ')
    gc.collect()

