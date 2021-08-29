import time
import pymysql as sql
from personInOutCheckConnection import sendMessage
from extConfig import inOutManageConfig as iomConfig

getMaxIndexQry = 'select max(lg_idx) as max_index from m_smart_log;'
getLatestLogQry = 'select a.lg_idx, a.datetime as ftime, a.evt as eventNo, a.`inout`, a.army_id, a.location_id, a.ac_user_id, a.evt_nm as evt_name, b.army_name, b.location_name from m_smart_log as a inner join m_army as b on a.location_id=b.location_id where datetime = (SELECT max(datetime) FROM m_smart_log);'


def getInitIndex():
    indexCnt = 0
    conn = sql.connect(host=iomConfig.iomHost, port=iomConfig.port, user=iomConfig.dbUserId, password=iomConfig.dbUserPw, db=iomConfig.db, charset='utf8')
    conn.ping(reconnect=True)
    with conn.cursor(sql.cursors.DictCursor) as cursor:
        cursor.execute(getMaxIndexQry)
        row = cursor.fetchone()
        indexCnt = row['max_index']
    return indexCnt


def check(index):
    conn = sql.connect(host=iomConfig.iomHost, port=iomConfig.port, user=iomConfig.dbUserId, password=iomConfig.dbUserPw, db=iomConfig.db, charset='utf8')
    conn.ping(reconnect=True)
    with conn.cursor(sql.cursors.DictCursor) as cursor:
        cursor.execute(getLatestLogQry)
        row = cursor.fetchone()
        now = int(time.time())

        print(row)
        rowNo = row['lg_idx']
        if row['eventNo'] not in iomConfig.authList:
            if index < row['lg_idx']:
                conn.close()
                return {"flag": True, "row": row, "index" : rowNo}
            else:
                conn.close()
                return {"flag": False, "row": None, "index": rowNo}
        else:
            conn.close()
            return {"flag": False, "row": None, "index": rowNo}
        # if int(row['ftime']) + (iomConfig.interval/1000) > now:
        #     conn.close()
        #     return {"flag": True, "row": row}
        # else:
        #     conn.close()
        #     return {"flag": False, "row": None}


getIndex = getInitIndex()
def run():
    global getIndex
    index = getIndex
    try:
        getData = check(index)
        getIndex = getData["index"]
        if getData["flag"]:
            sendMessage.makeEventMsg(getData["row"])
        time.sleep(iomConfig.interval / 1000)
    except Exception as e:
        print(e)

# def run():
#     index = getInitIndex()
#     while True:
#         try:
#             getData = check(index)
#             index = getData["index"]
#             if getData["flag"]:
#                 sendMessage.makeEventMsg(getData["row"])
#             time.sleep(iomConfig.interval / 1000)
#         except Exception as e:
#             print(e)
#             continue

