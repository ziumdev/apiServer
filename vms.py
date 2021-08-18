from psycopg2.extras import RealDictCursor
import psycopg2
from apiServerConfig import vmsConfig

qry = "SELECT" \
      "a.server_name, b.device_id, b.device_name, b.ip_address, b.port, b.install_location, b.latitude as utm_x, b.longitude as utm_y, b.utm_z, d.server_session" \
      "FROM AST_SERVER_INFO AS a" \
      "INNER JOIN AST_DEVICE_INFO AS b" \
      "ON a.server_name=b.server_name" \
      "INNER JOIN AST_INPUT_SESSION AS c" \
      "ON b.device_id = c.device_id" \
      "INNER JOIN AST_SERVER_SESSION AS d" \
      "on c.input_session_name = d.input_session_name" \
      "WHERE d.session_type = 'STREAM' "


def getVmsList():
    conn = psycopg2.connect(host=vmsConfig.vmsHost, port=vmsConfig.vmsdbPort, user=vmsConfig.vmsDbUserId,
                          password=vmsConfig.vmsDbPassword, dbname=vmsConfig.dbName)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(qry)
    rows = cursor.fetchall()
    result = {
        "count" : len(rows),
        "list": rows
    }
    print(result)
    conn.close()
    return rows

