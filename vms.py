from psycopg2.extras import RealDictCursor
import psycopg2
from apiServerConfig import vmsConfig
import mgrs

qry = "SELECT '" \
      + vmsConfig.vmsHost+"' as server_name, b.device_id, b.device_name, b.ip_address, b.port, b.install_location, b.latitude as utm_x, b.longitude as utm_y, b.utm_z_s, d.server_session" \
      " FROM AST_SERVER_INFO AS a" \
      " INNER JOIN AST_DEVICE_INFO AS b" \
      " ON a.server_name=b.server_name" \
      " INNER JOIN AST_INPUT_SESSION AS c" \
      " ON b.device_id = c.device_id" \
      " INNER JOIN AST_SERVER_SESSION AS d" \
      " on c.input_session_name = d.input_session_name" \
      " WHERE d.session_type = 'STREAM' and d.server_session like '%_F' "

fenceQry = " select '" \
        + vmsConfig.vmsHost+"' as server_name, b.device_id, b.device_name, b.ip_address, b.port, b.install_location, b.purpose," \
            " b.latitude as utm_x, b.longitude as utm_y, b.utm_z_s, d.server_session " \
            " from public.AST_SERVER_INFO AS a" \
            " INNER JOIN public.AST_DEVICE_INFO AS b" \
            " ON a.server_name=b.server_name" \
            " INNER JOIN public.AST_INPUT_SESSION AS c" \
            " ON b.device_id = c.device_id" \
            " INNER JOIN public.AST_SERVER_SESSION AS d" \
            " on c.input_session_name = d.input_session_name" \
            " WHERE d.session_type = 'STREAM' and " \
            " d.server_session like '%_F' and" \
            " b.purpose not like '%(병력생활)';"

livingQry = " select '" \
            + vmsConfig.vmsHost + "' as server_name, b.device_id, b.device_name, b.ip_address, b.port, b.install_location, b.purpose," \
            " b.latitude as utm_x, b.longitude as utm_y, b.utm_z_s, d.server_session " \
            " from public.AST_SERVER_INFO AS a" \
            " INNER JOIN public.AST_DEVICE_INFO AS b" \
            " ON a.server_name=b.server_name" \
            " INNER JOIN public.AST_INPUT_SESSION AS c" \
            " ON b.device_id = c.device_id" \
            " INNER JOIN public.AST_SERVER_SESSION AS d" \
            " on c.input_session_name = d.input_session_name" \
            " WHERE d.session_type = 'STREAM' and " \
            " d.server_session like '%_F' and" \
            " b.purpose like '%(병력생활)';"



def getVmsList():
    conn = psycopg2.connect(host=vmsConfig.vmsHost, port=vmsConfig.vmsdbPort, user=vmsConfig.vmsDbUserId,
                          password=vmsConfig.vmsDbPassword, dbname=vmsConfig.dbName)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(qry)
    rows = cursor.fetchall()
    mgrs_object = mgrs.MGRS()

    for row in rows:
        try:
            lat, lon = mgrs_object.toLatLon(row['utm_z_s'])
            row['utm_x'] = lon
            row['utm_y'] = lat
            print(row)
        except Exception as e:
            row['utm_x'] = 0
            row['utm_y'] = 0
    result = {
        "count": len(rows),
        "list": rows
    }
    print(result)
    conn.close()
    return result


def getFenceCctvList():
    conn = psycopg2.connect(host=vmsConfig.vmsHost, port=vmsConfig.vmsdbPort, user=vmsConfig.vmsDbUserId,
                          password=vmsConfig.vmsDbPassword, dbname=vmsConfig.dbName)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(fenceQry)
    rows = cursor.fetchall()
    mgrs_object = mgrs.MGRS()

    for row in rows:
        try:
            lat, lon = mgrs_object.toLatLon(row['utm_z_s'])
            row['utm_x'] = lon
            row['utm_y'] = lat
            print(row)
        except Exception as e:
            row['utm_x'] = 0
            row['utm_y'] = 0
    result = {
        "count": len(rows),
        "list": rows
    }
    print(result)
    conn.close()
    return result


def getLivingCctvList():
    conn = psycopg2.connect(host=vmsConfig.vmsHost, port=vmsConfig.vmsdbPort, user=vmsConfig.vmsDbUserId,
                          password=vmsConfig.vmsDbPassword, dbname=vmsConfig.dbName)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(livingQry)
    rows = cursor.fetchall()
    mgrs_object = mgrs.MGRS()

    for row in rows:
        try:
            lat, lon = mgrs_object.toLatLon(row['utm_z_s'])
            row['utm_x'] = lon
            row['utm_y'] = lat
            print(row)
        except Exception as e:
            row['utm_x'] = 0
            row['utm_y'] = 0
    result = {
        "count": len(rows),
        "list": rows
    }
    print(result)
    conn.close()
    return result


def getCctvListByPage(pageNo):
    if pageNo <= 0 :
        pageNo = 1

    conn = psycopg2.connect(host=vmsConfig.vmsHost, port=vmsConfig.vmsdbPort, user=vmsConfig.vmsDbUserId,
                          password=vmsConfig.vmsDbPassword, dbname=vmsConfig.dbName)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(fenceQry)
    rows = cursor.fetchall()
    mgrs_object = mgrs.MGRS()

    returnRow = []
    startNo = (pageNo-1) * 9
    endNo = pageNo * 9

    for row in rows:
        try:
            lat, lon = mgrs_object.toLatLon(row['utm_z_s'])
            row['utm_x'] = lon
            row['utm_y'] = lat
        except Exception as e:
            row['utm_x'] = 0
            row['utm_y'] = 0
    for row in list(rows[startNo:endNo]):
        if row != None:
            returnRow.append(row)

    print(returnRow)
    result = {
        "count": len(returnRow),
        "list": returnRow
    }
    # print(result)
    conn.close()
    return result
