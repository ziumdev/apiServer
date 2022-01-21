import time
import pymysql as sql
from lmsConnection import sendMessage
from extConfig import lmsConfig


# checkQry = 'SELECT count(*) as cnt FROM lms_event_info;'
getLatestLogQry = "select 장비명 as obj, 장비종류 as kind, IP, unix_timestamp(이벤트발생시각) as ftime, 이벤트등급 as eventLevel, 이벤트메시지 as eventMessage, 이벤트판단조건 as eventLogic, 그룹 as armyName from lms_event_info where unix_timestamp(이벤트발생시각) = (SELECT max(unix_timestamp(이벤트발생시각)) FROM lms_event_info) and 그룹='3대대' ;"

def getInitCnt():
    conn = sql.connect(host=lmsConfig.lmsHost, port=lmsConfig.port, user=lmsConfig.dbUserId, password=lmsConfig.dbUserPw, db=lmsConfig.db, charset='utf8')
    conn.ping(reconnect=True)
    with conn.cursor(sql.cursors.DictCursor) as cursor:
        cursor.execute(getLatestLogQry)
        row = cursor.fetchone()
        if row is None:
            return int(time.time())
        conn.close()
        return row["ftime"]


def check(maxFtime):
    conn = sql.connect(host=lmsConfig.lmsHost, port=lmsConfig.port, user=lmsConfig.dbUserId, password=lmsConfig.dbUserPw, db=lmsConfig.db, charset='utf8')
    conn.ping(reconnect=True)
    with conn.cursor(sql.cursors.DictCursor) as cursor:
        cursor.execute(getLatestLogQry)
        row = cursor.fetchone()
        if row is not None:
            if int(row['ftime']) > maxFtime:
                conn.close()
                return {"flag": True, "row": row}
            else:
                conn.close()
                return {"flag": False, "row": None}
        else:
            return {"flag": False, "row":None}

getMaxFtime = getInitCnt()

def run():
    global getMaxFtime
    maxFtime = getMaxFtime
    # main 에서 루프를 도는 함수
    getData = check(maxFtime)
    if getData["flag"]:
        getMaxFtime=getData['row']['ftime']
        sendMessage.makeEventMsg(getData["row"])


# def run():
#     maxFtime = getInitCnt()
#     while True:
#         getData = check(maxFtime)
#         if getData["flag"]:
#             maxFtime=getData['row']['ftime']
#             sendMessage.makeEventMsg(getData["row"])
#         time.sleep(lmsConfig.interval / 1000)

