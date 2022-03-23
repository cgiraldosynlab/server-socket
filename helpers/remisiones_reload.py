import os, sys
p = os.path.abspath('.')
sys.path.insert(1, p)

from config.db import Database

def reload_blaulab():
    try:
        db = Database()
        rows = db.query(
            '''
                select rd.rd_id           as id
                    , rd.rd_fecha_creacion
                    + rd.rd_hora_creacion as FecHora
                    , rd.rd_pac_ref       as referencia
                    , rd.rd_enviado       as enviado
                    , rd.rd_error         as error
                    , rd.rd_ack           as ack
                    , rd.rd_origen        as origen
                    , rd.rd_destino       as destino
                    , rd.rd_envios        as cant_envios
                 from interconnect.remision_det rd
                where rd.rd_fecha_creacion >= CURRENT_DATE-10
                  and rd.rd_destino         = %s
                  and rd.rd_ack         ilike %s
             order by rd.rd_id desc
            ''',
            ('LABCONOUS', '%Microsoft MSXML is not installed%')
        )
        if len(rows) > 0:
            print('cantidad de registros a procesado:', len(rows))
            int_proc = 0
            for row in rows:
                int_proc += 1
                sql_update = 'update interconnect.remision_det '
                sql_update += 'set rd_ack = null'
                sql_update += ', rd_enviado = false'
                sql_update += ', rd_error = false '
                sql_update += 'where rd_id = %s'
                sql_update += ' and rd_ack = %s'

                if db.update(sql_update, (row.id, 'Microsoft MSXML is not installed')):
                    print('--> mensaje: {} | id: {} | referencia: {}'.format('reiniciando remisión', row.id, row.referencia))
                else:
                    print('--> mensaje: {} | id: {} | referencia: {}'.format('error al reiniciar la orden ', row.id, row.referencia))
            else:
                print('proceso finalizado', '| cantidad procesado:', int_proc)
        else:
            print('no se encontraron registros para reenviar')
    except Exception as e:
        print('error:', e)

reload_blaulab()