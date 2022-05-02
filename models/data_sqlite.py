import datetime
from config.db import SQLite

class LogApp(SQLite):

    __NAME__ = '__logapp__'

    def __init__(self, mensaje):
        super().__init__()
        try:
            self.content = mensaje
            sql = 'insert into t010_log_app (f010_content, f010_notify, f010_show)'
            sql += 'values (?, False, False)'
            self.cursor.execute(sql, (self.content, ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f'{self.__NAME__}|__init__', e)

class Usuario(SQLite):

    __NAME__ = '__Usuario__'

    __id = -1
    __username = None
    __password = None
    __active = False
    __delete = False,
    __createAt = None
    __isFound = False

    def __init__(self, user):
        try:
            super().__init__()
            self.__user = user
            sql_text = '''
              select f001_id        as id
                   , f001_username  as username
                   , f001_password  as password
                   , f001_active    as active
                   , f001_create_at as createat
                from t001_users 
               where f001_username = ?
                 and f001_delete   = false '''

            self.cursor.execute(sql_text,(self.__user, ))
            rows = self.cursor.fetchall()

            if len(rows) > 0:
                for row in rows:
                    self.__id = row['id']
                    self.__username = row['username']
                    self.__password = row['password']
                    self.__active = row['active']
                    self.__createAt = row['createat']
                    self.__isFound = True
            else:
                self.__user = user
                self.__isFound = False
        except Exception as e:
            LogApp(mensaje=f'__Usuario__| __init__ | {e}')

    def __clear(self):
        self.__id = None
        self.__user = None
        self.__password = None
        self.__active = False
        self.__delete = False
        self.__createAt = None

    def guardar(self):
        try:
            if self.__isFound:
                pass
            else:
                pass
            return True
        except Exception as e:
            LogApp(f'__Usuario__ | guardar | {e}')

    def delete(self):
        if self.__isFound:
            if self.cursor.execute('DELETE FROM t001_users WHERE f001_id = ?', (self.__user)).rowcount > 0:
                print(f'usuario eliminado con éxito')

    def get_id(self) -> int:
        return self.__id

    def set_id(self, id) -> None:
        if not self.__isFound:
            self.__id = id

    def get_user(self) -> str:
        return self.__user

    def set_user(self, user):
        self.__user = user

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_createAt(self):
        return self.__createAt

    def get_isFound(self):
        return self.__isFound

class TipoDocumento(SQLite):

    __NAME__ = '__TipoDocumento__'

    __id = -1
    __code = ''
    __name = ''
    __active = False
    __delete = False
    __createAt = None
    __isFound = False

    def __init__(self, codigo):
        try:
            super().__init__()
            self.__code = codigo.strip()
            if codigo and codigo != '':
                sql_text = '''
                      select f002_id        AS id
                           , f002_code      as code 
                           , f002_name      as name
                           , f002_active    as active
                           , f002_create_at as createAt
                        from t002_types_documents td
                       where td.f002_code = ? '''

                self.cursor.execute(sql_text, (self.__code, ))
                rows = self.cursor.fetchall()
                for row in rows:
                    self.__id = row['id']
                    self.__code = row['code']
                    self.__name = row['name']
                    self.__active = row['active']
                    self.__createAt = row['createAt']
                    self.__isFound = True
        except Exception as e:
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def guardar(self) -> bool:
        try:
            if self.__isFound == False:
                sql = 'insert into t002_types_documents(f002_code, f002_name, f002_active, f002_delete, f002_f001_id)'
                sql += 'values(?, ?, ?, False, 1)'
                params = (
                    self.__code,
                    self.__name,
                    self.__active
                )
                self.cursor.execute(sql, params)
                if self.cursor.rowcount:
                    self.__id = self.cursor.lastrowid
            else:
                sql = 'update t002_types_documents set f002_name = ?, f002_active = ? where f002_id = ?'
                params = (
                    self.__name,
                    self.__active,
                    self.__id
                )
                self.cursor.execute(sql, params)

            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | __init__ | {e} | {self.__code}-{self.__name}')

    def set_code(self, code):
        self.__code = code

    def set_name(self, name):
        self.__name = name

    def set_active(self, active):
        self.__active = active

    def get_id(self):
        return self.__id

    def get_code(self):
        return self.__code

    def get_name(self):
        return self.__name

    def get_active(self):
        return self.__active

    def get_createAt(self):
        return self.__createAt

    def get_isfound(self):
        return self.__isFound

class Paciente(SQLite):

    __NAME__ = '__Paciente__'

    id = None
    tipodoc = None
    number = None
    first_name = None
    second_name = None
    last_name = None
    middle_name = None
    birthdate = None
    gender = None
    expedition_date = None
    blood_type = None
    address = None
    phone = None
    cellphone = None
    email = None
    createAt = None
    updateAt = None
    isActive = False
    isDelete = False
    createBy = None
    isFound = False
    
    def __init__(self, tipodoc: TipoDocumento, number: str):
        try:
            super().__init__()

            self.tipodoc = tipodoc.get_id()
            self.number = number

            if (tipodoc is not None) and (tipodoc.get_isfound() != False) and number is not None:

                sql_text = '''
                        select tp.f003_id               as id 
                             , tp.f003_f002_id          as tpdoc_id
                             , ttd.f002_code            as tpdoc_code
                             , tp.f003_number           as number
                             , tp.f003_first_name       as first_name
                             , tp.f003_second_name      as second_name
                             , tp.f003_last_name        as last_name
                             , tp.f003_middle_name      as middle_name
                             , tp.f003_birth_date       as birthdate
                             , tp.f003_gender           as gender
                             , tp.f003_expedition_date  as expedition
                             , tp.f003_blood_type       as blood_type
                             , tp.f003_address          as address
                             , tp.f003_phone            as phone
                             , tp.f003_cell_phone       as cellphone
                             , tp.f003_email            as email
                             , tp.f003_create_at        as createAt
                             , tp.f003_update_at        as updateAt
                             , tp.f003_active           as isActive
                             , tp.f003_delete           as isDelete
                             , tp.f003_f001_id          as craateby_id
                             , tu.f001_username         as createby
                          from t003_patients         tp
                    inner join t002_types_documents ttd ON ttd.f002_id = tp.f003_f002_id
                    inner join t001_users            tu ON tu.f001_id  = tp.f003_f001_id
                         where tp.f003_f002_id = ?
                           AND tp.f003_number  = ?  '''
                params = (tipodoc.get_id(), number)

                self.cursor.execute( sql_text, params )
                rows = self.cursor.fetchall()

                if len(rows) > 0:
                    for row in rows:
                        try:
                            self.id = row['id']
                            self.first_name = row['first_name']
                            self.second_name = row['second_name']
                            self.last_name = row['last_name']
                            self.middle_name = row['middle_name']
                            self.birthdate = row['birthdate']
                            self.gender = row['gender']
                            self.expedition_date = row['expedition']
                            self.blood_type = row['blood_type']
                            self.address = row['address']
                            self.phone = row['phone']
                            self.cellphone = row['cellphone']
                            self.email = row['email']
                            self.createAt = row['createAt']
                            self.updateAt = row['updateAt']
                            self.isActive = row['isActive']
                            self.isDelete = row['isDelete']
                            self.createBy = row['craateby_id']
                            self.isFound = True
                        except Exception as e:
                            print(e)
        except Exception as e:
            LogApp(f'{self.__NAME__} | __init__ | {e}')
    
    def guardar(self, **kwargs):
        registry = False
        if len(kwargs) > 0:

            if kwargs.get('typeId'):
                self.tipodoc = kwargs.get('typeId')
            else:
                self.tipodoc = -1
            if kwargs.get('numberId'):
                self.number = kwargs.get('numberId')
            else:
                self.number = ''
            if kwargs.get('first_name'):
                self.first_name = kwargs.get('first_name')
            else:
                self.first_name = ''
            if kwargs.get('second_name'):
                self.second_name = kwargs.get('second_name')
            else:
                self.second_name = ''
            if kwargs.get('last_name'):
                self.last_name = kwargs.get('last_name')
            else:
                self.last_name = ''
            if kwargs.get('middle_name'):
                self.middle_name = kwargs.get('middle_name')
            else:
                self.middle_name = ''
            if kwargs.get('birth_date'):
                self.birthdate = kwargs.get('birth_date')
            else:
                self.birthdate = ''
            if kwargs.get('gender'):
                if kwargs.get('gender') != '':
                    self.gender = kwargs.get('gender')
                else:
                    self.gender = 'I'
            else:
                self.gender = 'I'
            if kwargs.get('expedition'):
                self.expedition_date = kwargs.get('expedition')
            else:
                self.expedition_date = ''
            if kwargs.get('blood_type'):
                self.blood_type = kwargs.get('blood_type')
            else:
                self.blood_type = ''
            if kwargs.get('address'):
                self.address = kwargs.get('address')
            else:
                self.address = ''
            if kwargs.get('phone'):
                self.phone = kwargs.get('phone')
            else:
                self.phone = ''
            if kwargs.get('cellphone'):
                self.cellphone = kwargs.get('cellphone')
            else:
                self.cellphone = ''
            if kwargs.get('email'):
                self.email = kwargs.get('email')
            else:
                self.email = ''
            if kwargs.get('active'):
                self.isActive = kwargs.get('active')
            else:
                self.isActive = True
            self.isDelete = False

            if not self.isFound:
                try:
                    sql_insert = '''
                        INSERT INTO t003_patients 
                            ( f003_f002_id, f003_number, f003_first_name, f003_second_name, f003_last_name, f003_middle_name
                            , f003_birth_date, f003_gender, f003_expedition_date, f003_blood_type, f003_address, f003_phone
                            , f003_cell_phone, f003_email, f003_active, f003_delete, f003_f001_id )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1) '''
                    insert_params = (self.tipodoc, self.number, self.first_name, self.second_name, self.last_name,
                                     self.middle_name, self.birthdate, self.gender, self.expedition_date, self.blood_type,
                                     self.address, self.phone, self.cellphone, self.email, self.isActive, self.isDelete )
                    self.cursor.execute(sql_insert, insert_params)
                    rowAffected = self.cursor.rowcount
                    self.conn.commit()
                    if self.cursor.rowcount > 0:
                        self.id = self.cursor.lastrowid
                    return rowAffected > 0
                except Exception as e:
                    self.conn.rollback()
                    LogApp(f'{self.__NAME__} | guardar | insert | {e} | ')
            else:
                try:
                    sql_update = '''
                        UPDATE t003_patients
                           SET f003_first_name = ?
                             , f003_second_name = ?
                             , f003_last_name = ?
                             , f003_middle_name = ?
                             , f003_birth_date = ?
                             , f003_gender = ?
                             , f003_expedition_date = ?
                             , f003_blood_type = ?
                             , f003_address = ?
                             , f003_phone = ?
                             , f003_cell_phone = ?
                             , f003_email = ?
                             , f003_active = ?
                             , f003_delete = ?
                         WHERE f003_id = ?
                           AND f003_f002_id = ?
                           AND f003_number = ? '''
                    update_params = (self.first_name, self.second_name, self.last_name, self.middle_name, self.birthdate, self.gender,
                                     self.expedition_date, self.blood_type, self.address, self.phone, self.cellphone, self.email,
                                     self.isActive, self.isDelete, self.id, self.tipodoc, self.number)
                    self.cursor.execute(sql_update, update_params)
                    rowAffected = self.cursor.rowcount
                    self.conn.commit()
                    return rowAffected > 0
                except Exception as e:
                    self.conn.rollback()
                    LogApp(f'{self.__NAME__} | guardar | update | {e}')
        return registry
    
    def delete(self):
        try:
            return self.update('UPDATE t003_patients SET f003_delete = 1 WHERE f003_f002_id = ? AND f003_number = ?', (self.tipodoc, self.number))
        except Exception as e:
            datos = f'{self.tipodoc}¬{self.number}¬{self.first_name}¬{self.second_name}¬'
            datos += f'{self.last_name}¬{self.middle_name}¬{self.birthdate}¬{self.gender}¬'
            datos += f'{self.expedition_date}¬{self.blood_type}¬{self.address}¬{self.phone}¬'
            datos += f'{self.cellphone}¬{self.email}¬{self.isActive}¬{self.isDelete}'
            #print(datos)
            LogApp(f'{self.__NAME__} | delete | {e}')

    def __str__(self):
        return f'{self.id} - {self.tipodoc} - doc: {self.number} - {self.first_name} - {self.second_name} - {self.last_name} - {self.middle_name} - {self.birthdate} - {self.gender} - {self.expedition_date} - {self.blood_type} - {self.address} - {self.phone} - {self.cellphone} - {self.email}'

class Ubicacion(SQLite):

    __NAME__ = 'Ubicacion'

    id = None
    code = None
    name = None
    isActive = None
    isDelete = None
    createAt = None
    createBy = None
    isFound = False

    def __init__(self, codigo):
        super().__init__()
        self.code = codigo
        try:
            if codigo and codigo != '':
                self.cursor.execute('''
                    select f004_id        as id
                         , f004_create_at as createAt
                         , f004_code      as code
                         , f004_name      as name
                         , f004_active    as isActive
                         , f004_delete    as isDelete
                         , f004_f001_id   as createBy
                      from t004_locations tl
                     where f004_code   = ?
                       and f004_delete = false''', (self.code,))
                rows = self.cursor.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        self.id = int(row['id'])
                        self.name = row['name']
                        self.isActive = row['isActive']
                        self.isDelete = row['isDelete']
                        self.createBy = row['createBy']
                        self.createAt = row['createAt']
                        self.isFound = True
        except Exception as e:
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def guardar(self):
        if self.isFound:
            try:
                sql = 'INSERT INTO t004_locations (f004_code, f004_name, f004_active, f004_delete, f004_f001_id) VALUES (?, ?, ?, ?, ?)'
                params = (self.code, self.name, self.isActive, self.isDelete, 1)
                self.cursor(sql, params)
                rowAffected = self.cursor.rowcount
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | guardar | insert | {e}')
        else:
            try:
                sql = 'update t004_locations set f004_name = ?, f004_active = ? where f004_id = ? and f004_code = ?'
                params = (self.name, self.isActive, self.id, self.code)
                self.cursor(sql, params)
                rowAffected = self.cursor.rowcount
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | guardar | update | {e} | {self.code}¬{self.name}')

    def delete(self):
        if self.isFound:
            try:
                self.cursor('update t004_locations set f004_delete = true where f004_id = ?', (self.id, ))
                rowAffected = self.cursor.fetchall()
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                LogApp(f'{self.__NAME__} | delete | {e}')

class Servicio(SQLite):

    __NAME__ = 'Servicio'

    id = None
    code = None
    name = None
    isActive = None
    isDelete = None
    createAt = None
    createBy = None
    isFound = False

    def __init__(self, codigo):
        super().__init__()
        self.code = codigo
        try:
            if codigo and codigo != '':
                self.cursor.execute('''
                    select f005_id        as id
                         , f005_create_at as createAt
                         , f005_code      as code
                         , f005_name      as name
                         , f005_active    as isActive
                         , f005_delete    as isDelete
                         , f005_f001_id   as createBy
                      from t005_services 
                     where f005_code   = ?
                       and f005_delete = false''', (self.code,))
                rows = self.cursor.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        self.id = row['id']
                        self.name = row['name']
                        self.isActive = row['isActive']
                        self.isDelete = row['isDelete']
                        self.createBy = row['createBy']
                        self.createAt = row['createAt']
                        self.isFound = True
        except Exception as e:
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def guardar(self):
        if self.isFound:
            try:
                sql = 'INSERT INTO t005_services (f005_code, f005_name, f005_active, f005_delete, f005_f001_id) VALUES (?, ?, ?, ?, ?)'
                params = (self.code, self.name, self.isActive, self.isDelete, 1)
                self.cursor(sql, params)
                if self.cursor.rowcount > 0:
                    self.id = self.cursor.lastrowid
                self.conn.commit()
                return self.cursor.rowcount > 0
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | guardar | insert | {e}')
        else:
            try:
                sql = 'update t005_services set f005_name = ?, f005_active = ? where f005_id = ? and f005_code = ?'
                params = (self.name, self.isActive, self.id, self.code)
                self.cursor(sql, params)
                rowAffected = self.cursor.rowcount
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | guardar | update | {e}')

    def delete(self):
        if self.isFound:
            try:
                self.cursor('update t005_services set f005_delete = true where f005_id = ?', (self.id, ))
                rowAffected = self.cursor.fetchall()
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                LogApp(f'{self.__NAME__} | delete | {e}')

class Empresa(SQLite):

    __NAME__ = '__Empresa__'

    id = None
    code = None
    name = None
    isActive = None
    isDelete = None
    createAt = None
    createBy = None
    isFound = False

    def __init__(self, codigo):
        super().__init__()
        self.code = codigo
        try:
            if codigo and codigo != '':
                self.cursor.execute('''
                    select f006_id        as id
                         , f006_create_at as createAt
                         , f006_code      as code
                         , f006_name      as name
                         , f006_active    as isActive
                         , f006_delete    as isDelete
                         , f006_f001_id   as createBy
                      from t006_companies 
                     where f006_code   = ?
                       and f006_delete = false''', (self.code,))
                rows = self.cursor.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        self.id = row['id']
                        self.name = row['name']
                        self.isActive = row['isActive']
                        self.isDelete = row['isDelete']
                        self.createBy = row['createBy']
                        self.createAt = row['createAt']
                        self.isFound = True
        except Exception as e:
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def guardar(self):
        if not self.isFound:
            try:
                sql = 'INSERT INTO t006_companies (f006_code, f006_name, f006_active, f006_delete, f006_f001_id) VALUES (?, ?, ?, ?, ?)'
                params = (self.code, self.name, self.isActive, self.isDelete, 1)
                self.cursor.execute(sql, params)
                if self.cursor.rowcount > 0:
                    self.id = self.cursor.lastrowid
                    self.isFound = True
                self.conn.commit()
                return self.cursor.rowcount > 0
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | guardar | insert | {e}')
        else:
            try:
                sql = 'update t006_companies set f006_name = ?, f006_active = ? where f006_id = ? and f006_code = ?'
                params = (self.name, self.isActive, self.id, self.code)
                self.cursor.execute(sql, params)
                rowAffected = self.cursor.rowcount
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | guardar | update | {e}')

    def delete(self):
        if self.isFound:
            try:
                self.cursor('update t006_companies set f006_delete = true where f006_id = ?', (self.id, ))
                rowAffected = self.cursor.fetchall()
                self.conn.commit()
                return rowAffected > 0
            except Exception as e:
                LogApp(f'{self.__NAME__} | delete | {e}')


class Test(SQLite):

    __NAME__ = 'Test'

    id = None
    code = None
    name = None
    active = False
    groupBy = None
    createAt = None
    isFound = False

    def __init__(self, code):
        super().__init__()
        try:
            self.code = code
            if code:
                sql = '''
                    select f012_id        as id
                         , f012_code      as code 
                         , f012_name      as name
                         , f012_active    as isActive
                         , f012_group_by  as group_by
                         , f012_create_at as createAt
                      from t012_test tt
                     where tt.f012_code = ? '''
                self.cursor.execute(sql, (code,))
                rows = self.cursor.fetchall()
                if rows:
                    for row in rows:
                        self.id = row['id']
                        self.name = row['name']
                        self.active = row['isActive']
                        self.groupBy = row['group_by']
                        self.createAt = row['createAt']
                        self.isFound = True
        except Exception as e:
            print('error al buscar el test', e)

    def guardar(self, **kwargs):
        try:
            if kwargs.get('code'):
                self.code = kwargs.get('code')
            if kwargs.get('name'):
                self.name = kwargs.get('name')
            if kwargs.get('isActive'):
                self.active = kwargs.get('isActive')
            if kwargs.get('groupBy'):
                self.groupBy = kwargs.get('groupBy')
            else:
                self.groupBy = 0

            ''' procesar muestra '''
            if not self.isFound:
                sql_insert = 'insert into t012_test (f012_code, f012_name, f012_active, f012_group_by) values (?, ?, ?, ?)'
                params_insert = (self.code, self.name, self.active, self.groupBy)
                self.cursor.execute(sql_insert, params_insert)
                if self.cursor.rowcount > 0:
                    self.id = self.cursor.lastrowid
                    self.isFound = True
            else:
                sql_update = 'update t012_test set f012_name = ?, f012_active = ?, f012_group_by = ? where f012_id = ?'
                params_update = (self.name, self.active, self.groupBy, self.id)
                self.cursor.execute(sql_update, params_update)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f'[x] ERROR | {self.__NAME__} | error: {e}')

class MensajeIn(SQLite):

    __NAME__ = 'MensajeIn'

    id = None
    createAt = None
    createBy = None
    sender = None
    sender_facility = None
    reception = None
    reception_facility = None
    control_id = None
    content = None
    response = None
    type = None
    isDelete = False
    processAt = None
    isFound = False

    def __init__(self, buscar, **kwargs):
        super().__init__()
        try:
            if buscar:
                pass
            else:
                self.sender = kwargs.get('sender')
                self.sender_facility = kwargs.get('sender_facility')
                self.reception = kwargs.get('reception')
                self.reception_facility = kwargs.get('reception_facility')
                self.control_id = kwargs.get('control_id')
                self.content = kwargs.get('content')
                self.type = kwargs.get('type')

                sql = 'insert into t007_messages '
                sql += '(f007_sender, f007_sender_facility, f007_reception, f007_reception_facility, f007_control_id, f007_content, f007_response, f007_type_message) '
                sql += 'values '
                sql += '(?, ?, ?, ?, ?, ?, ?, ?)'
                params = (self.sender, self.sender_facility, self.reception, self.reception_facility, self.control_id, self.content, '', self.type)

                self.cursor.execute(sql, params)
                if self.cursor.rowcount > 0:
                    self.id = self.cursor.lastrowid
                    self.isFound = True
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def delete_message(self):
        if self.isFound:
            try:
                self.cursor.execute('delete from t008_orders where f008_f007_id = ?', (self.id, ))
                self.cursor.execute('delete from t007_messages where f007_id = ?', (self.id, ))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                LogApp(f'{self.__NAME__} | delete_message | {e}')

    def set_response(self):
        try:
            if self.isFound:
                self.cursor.execute(
                    'update t007_messages set f007_response = ? where f007_id = ?',
                    (self.response, self.id)
                )
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | set_response | {e}')

    def cant_message(self, control_id):
        try:
            cantidad = 0
            if control_id:
                self.cursor.execute('select count(1) as cantidad from t007_messages tm where f007_control_id = ?', (control_id, ))
                rows = self.cursor.fetchall()
                if rows:
                    for row in rows:
                        cantidad = row['cantidad']
            return cantidad
        except Exception as e:
            LogApp(f'{self.__NAME__} | cant_message | {e}')

class MensajeError(SQLite):

    __NAME__ = 'MensajeError'

    id = None
    createAt = None
    createBy = None
    sender = None
    sender_facility = None
    reception = None
    reception_facility = None
    control_id = None
    content = None
    response = None
    type = None
    isDelete = False
    processAt = None
    isFound = False

    def __init__(self, buscar, **kwargs):
        super().__init__()
        try:
            if buscar:
                pass
            else:
                self.sender = kwargs.get('sender')
                self.sender_facility = kwargs.get('sender_facility')
                self.reception = kwargs.get('reception')
                self.reception_facility = kwargs.get('reception_facility')
                self.control_id = kwargs.get('control_id')
                self.content = kwargs.get('content')
                self.type = kwargs.get('type')

                sql = 'insert into t011_messages_error '
                sql += '(f011_sender, f011_sender_facility, f011_reception, f011_reception_facility, f011_control_id, f011_content, f011_response, f011_type_message) '
                sql += 'values '
                sql += '(?, ?, ?, ?, ?, ?, ?, ?)'
                params = (self.sender, self.sender_facility, self.reception, self.reception_facility, self.control_id, self.content, '', self.type)
                self.cursor.execute(sql, params)
                if self.cursor.rowcount > 0:
                    self.id = self.cursor.lastrowid
                    self.isFound = True
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def set_response(self):
        try:
            if self.isFound:
                self.cursor.execute('update t007_messages set f007_response = ? where f007_id = ?', (self.response, self.id))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | set_response | {e}')

class Orden(SQLite):

    __NAME__ = '__Orden__'

    # properties
    id = None
    number = None
    date = None
    time = None
    messageId = None
    patientId = None
    locationId = None # ubicación
    serviceId = None # servicios
    companyId = None # id de la compañia
    priority = None
    bed = None
    type_service = None # E: Empresa | P: Particular
    entity = None
    service = None
    createAt = None
    details = []
    isFound = False

    def __init__(self, **kwargs):
        super().__init__()
        try:
            self.number = kwargs.get('number')
            self.date = kwargs.get('date')
            self.time = kwargs.get('time')
            self.messageId = kwargs.get('messageId')
            self.patientId = kwargs.get('patientId')
            self.locationId = kwargs.get('locationId')
            self.serviceId = kwargs.get('serviceId')
            self.companyId = kwargs.get('companyId')
            self.priority = kwargs.get('priority')
            self.bed = kwargs.get('bed')
            self.type_service = kwargs.get('type')
            self.entity = kwargs.get('entity')
            self.history = kwargs.get('history')
            self.service = kwargs.get('service')

            sql = 'INSERT INTO t008_orders '
            sql += '(f008_number, f008_date, f008_time, f008_f007_id, f008_f003_id, f008_f004_id, f008_f005_id, f008_f006_id, f008_priority, f008_bed, f008_type_service, f008_entity, f008_history, f008_service)'
            sql += 'VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );'
            params = (
                self.number,
                self.date,
                self.time,
                self.messageId,
                self.patientId,
                self.locationId,
                self.serviceId,
                self.companyId,
                self.priority,
                self.bed,
                self.type_service,
                self.entity,
                self.history,
                self.service
            )
            self.cursor.execute(sql, params)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                self.isFound = True
                self.id = self.cursor.lastrowid

        except Exception as e:
            self.isFound = False
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | __init__ | {e}')

    def add_detail(self, **kwargs):
        try:
            pass
        except Exception as e:
            print('error:', e)

    def add_details(self, *args):
        try:
            if self.isFound:
                sql = 'INSERT INTO t009_details (f009_f008_id, f009_barcode, f009_sequence, f009_test, f009_name, f009_date_test)'
                sql += 'VALUES (?, ?, ?, ?, ?, ?)'
                for item in args:
                    for field in item:
                        #print(field.get('barcode'), field.get('sequence'), field.get('code'), field.get('name'), field.get('date_test'))
                        self.cursor.execute(sql, (
                            self.id,
                            field.get('barcode'),
                            int(field.get('sequence')),
                            field.get('code'),
                            field.get('name'),
                            field.get('date_test')
                        ))
                        self.details.append(field)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LogApp(f'{self.__NAME__} | add_details | {e}')