import datetime

from psycopg2.extras import RealDictCursor
import psycopg2
from apiServerConfig import carEntryConfig

getindexQry = 'select max(id) from incar'
incarQry = 'Insert into incar(id, created_at, updated_at, command, car_number, in_date_time, kind, lprid, owner_name, group_name, dept_name)' \
           'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
outCarQry = ''


def getIndex():
    conn = psycopg2.connect(host=carEntryConfig.carEntryHost, port=carEntryConfig.carEntryDbPort,
                            user=carEntryConfig.carEntryDbId, password=carEntryConfig.carEntryDbPassword,
                            dbname=carEntryConfig.dbName)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(getindexQry)
    row = cursor.fetchone()
    conn.close()
    return row


def carEvent(param):
    indexNo = getIndex()['id'] + 1
    now = datetime.datetime.now()
    conn = psycopg2.connect(host=carEntryConfig.carEntryHost, port=carEntryConfig.carEntryDbPort, user=carEntryConfig.carEntryDbId, password=carEntryConfig.carEntryDbPassword, dbname=carEntryConfig.dbName)
    cursor = conn.cursor()
    if param['command'] == 'smt_alert_incar':
        qryParameter = (indexNo,  # id
                        now,  # created_at
                        now,  # updated_at
                        param['command'],  # command
                        param['data']['car_number'],
                        param['data']['date_time'],
                        param['data']['kind'],
                        param['data']['lprid'],
                        param['data']['owner_name'],
                        param['data']['group_name'],
                        param['data']['dept_name']
                        )
        cursor.execute(incarQry, qryParameter)
        conn.commit()
        conn.close()
        return 'success'

    elif param['command'] == '"smt_alert_outcar':
        conn.commit()
        conn.close()
        return 'success'
    else:
        return 'fail'
