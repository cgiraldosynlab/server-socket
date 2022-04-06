import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    
    def __init__(self, **args):
        __ISCONNECT = False
        try:
            self.conn = None
            self.qry = None            

            # leer parametros de conexión de las variables de entorno del S.O
            #pg_host = os.environ['PG_HOST']
            #pg_port = os.environ['PG_PORT']
            #pg_username = os.environ['PG_USERNAME']
            #pg_password = os.environ['PG_PASSWORD']
            #pg_database = os.environ['PG_DATABASE']
            #pg_encoding = os.environ['PG_CHARSET']

            pg_host = '172.31.4.8'
            pg_port = '5432'
            pg_username = 'uwinsisdb'
            pg_password = '42931W1n4'
            pg_database = 'WINSISLAB'
            pg_encoding = 'LATIN1'

            self.conn = psycopg2.connect(
                host=pg_host,
                port=pg_port,
                dbname=pg_database,
                user=pg_username,
                password=pg_password
            )
            self.qry = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            rows = self.qry.execute('SELECT 1 + 1')
            if rows: 
                self.__ISCONNECT = True
                print('[x] conectado con la base de datos')
        except Exception as e:
            self.__ISCONNECT = False
            print('error:', e)

    def query(self, sql_text, params=None, one=False):
        try:
            if params is None:
                self.qry.execute(sql_text)
            else:
                self.qry.execute(sql_text, params)

            rows = None
            if one:
                rows = self.qry.fetchone()
            else:
                rows = self.qry.fetchall()
            return rows
        except Exception as e:
            print('error:', e)

    def insert(self, sql_insert, params) -> bool:
        try:
            if params is None:
                print('error: los parametros son obligatorios')
                return False
            else:
                self.qry.execute(sql_insert, params)
            self.conn.commit()
            return self.qry.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print('error:', e)

    def update(self, sql_update, params) -> bool:
        try:
            if params is None:
                print('error: los parametros son obligatorios')
                return False
            else:
                self.qry.execute(sql_update, params)
            self.conn.commit()
            return self.qry.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print('error:', e)

    def update_sql(self, sql_update):
        try:
            self.qry.execute(sql_update)
            self.conn.commit()
            return self.qry.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print('error:', e)

    def delete(self, sql_delete, params):
        try:
            if params is None:
                print('error: los parametros son obligataorios')
                return False
            else:
                self.qry.execute(sql_delete, params)
            self.conn.commit()
            return self.qry.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print('error:', e)

class SQLite:

    def __init__(self):
        try:
            ruta_db = os.path.dirname(__file__)
            self.conn = sqlite3.connect(f'{ruta_db}/synlab.db')
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

            # crear database
            if os.path.exists(f'{ruta_db}/backup.sql'):
                f = open(f'{ruta_db}/backup.sql')
                try:
                    self.cursor.execute('BEGIN TRANSACTION;')
                    scripts = f.read().split(';')
                    for script in scripts:
                        self.cursor.execute(script)
                    self.cursor.execute('COMMIT;')
                    f.close()
                    os.rename(f'{ruta_db}/backup.sql', f'{ruta_db}/backup_ok.sql')
                except Exception as e:
                    self.cursor.execute('ROLLBACK;')
                    print('error al restaurar la base de datos', e)
        except Exception as e:
            print('error:', e)