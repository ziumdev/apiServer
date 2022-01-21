import json, datetime, struct, socket
import time
from apiServerConfig import lidarConfig
from extConfig import mrsConfig
import uuid
import mgrs

lidarFlag = True
lidarInterval = lidarConfig.eventInterval
priorTime = int(time.time())


def check():
    global lidarFlag
    global priorTime
    now = int(time.time())
    if lidarFlag:
        lidarFlag = False
        return True
    else:
        if priorTime + int(lidarInterval / 1000) < now:
            priorTime = now
            return True
        else:
            return False


def lidarEventProcess(param):
    if check():
        mgrsObject = mgrs.MGRS()

        stdCd = mrsConfig.mrsClientCd + '-' + mrsConfig.mrsSiteCd + '-' + '000' + mrsConfig.lidarEventCode
        bodyJson = mrsConfig.bodyJson
        uSvcOutbId = str(uuid.uuid4())[:24]
        statEvetNm = '라이다 비정상 물체 탐지'
        eventNo = param['lidar']['Id']
        statEvetId = stdCd + '001' + 'E' + str(23)
        dataKey = 'objectNum'
        dataValue = param['objectNum']
        statEvetItem = [{'key': dataKey, 'value': dataValue}]  # objectNum
        mgrsCoordinate = mgrsObject.UTMToMGRS(zone=52, hemisphere='N', easting=param['lidar']['UTM_X'], northing=param['lidar']['UTM_Y'])
        longlat = mgrsObject.toLatLon(mgrsCoordinate)
        mgrsCoordinate = mgrsCoordinate[0:3] + ' ' + mgrsCoordinate[3:5] + ' ' + mgrsCoordinate[5:10] + ' ' + mgrsCoordinate[10:15]
        longitude = longlat[0]
        latitude = longlat[1]

        # 라이다 임시처리
        # longitude = '37.65456380916093'
        # latitude = '126.77170671397928'
        # mgrsCoordinate = '52S CG 03435 69825'
        eventMsg = mgrsCoordinate + '에서 비정상 물체 발견'
        print(mgrsCoordinate)

        bodyJson["StatEvet"]["uSvcOutbId"] = uSvcOutbId
        bodyJson["StatEvet"]["statEvetId"] = statEvetId
        bodyJson["StatEvet"]["statEvetNm"] = statEvetNm
        bodyJson["StatEvet"]["statEvetGdCd"] = '00'
        bodyJson["StatEvet"]["procSt"] = 1
        bodyJson["StatEvet"]["outbPosCnt"] = 1
        bodyJson["StatEvet"]["outbPosNm"] = statEvetNm
        bodyJson["StatEvet"]["statEvetCntn"] = eventMsg
        bodyJson["StatEvet"]["statEvetOutbDtm"] = ''
        bodyJson["StatEvet"]["statEvetItemCnt"] = 1
        bodyJson["StatEvet"]["statEvetItem"] = statEvetItem
        bodyJson["StatEvet"]["cpxRelEvetOutbSeqnCnt"] = 0
        location = [{
            'y': latitude,
            'x': longitude,
            'z': '0'
        }]
        bodyJson["StatEvet"]["outbPos"] = location

        print("ERS msg")
        print(bodyJson)
        sendToErs(bodyJson)
        return 0


def sendMsg(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((mrsConfig.mrsHost, mrsConfig.mrsPort))
    sock.send(msg)
    sock.close()


def sendToErs(jsonData):
    currentDateTimeString = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    headerA = mrsConfig.mrsClientCd + '     ' + mrsConfig.mrsSiteCd + 'A1' + '      ' + mrsConfig.sendSystemCd + " "
    headerB = mrsConfig.headerTypeCd + mrsConfig.traceId + currentDateTimeString
    jsonData['StatEvet']['statEvetOutbDtm'] = currentDateTimeString
    bodyByte = json.dumps(jsonData, ensure_ascii=False).encode('utf-8')  # Json 값을 byte로 변경
    bodyLength = struct.pack('<I', bodyByte.__len__())
    header = headerA.encode('utf-8').__add__(bodyLength).__add__(headerB.encode('utf-8'))
    msg = header + bodyByte
    sendMsg(msg)
