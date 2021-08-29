import socket, uuid
from extConfig import mrsConfig, inOutManageConfig as iomConfig
import datetime, json, struct


def sendMsg(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((mrsConfig.mrsHost, mrsConfig.mrsPort))
    sock.send(msg)
    sock.close()


def makeEventMsg(data):
    statEvetNm = ''
    if data['inout'] == 1:
        statEvetNm = '탄약고 진입'
    elif data['inout'] == 2:
        statEvetNm = '탄약고 진출'

    stdCd = mrsConfig.mrsClientCd + '-' + mrsConfig.mrsSiteCd + '-' + '000' + mrsConfig.iomEventCode
    bodyJson = mrsConfig.bodyJson

    uSvcOutbId = str(uuid.uuid4())[:24]
    statEvetId = stdCd + '001' + 'E' + str(21)

    dataKey = 'InOut'
    dataValue = data['inout']
    statEvetItem = [{'key': dataKey, 'value': dataValue}]

    eventMsg = data['army_name'] + ' ' + data['location_name'] + ' ' + data['evt_name']

    bodyJson["StatEvet"]["statEvetId"] = statEvetId
    bodyJson["StatEvet"]["uSvcOutbId"] = uSvcOutbId
    bodyJson["StatEvet"]["statEvetNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetGdCd"] = '00' # 탄약고 출입은 등급이 없음
    bodyJson["StatEvet"]["procSt"] = 1
    bodyJson["StatEvet"]["outbPosCnt"] = 1
    bodyJson["StatEvet"]["outbPosNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetCntn"] = eventMsg + ' 이벤트 발생'
    bodyJson["StatEvet"]["statEvetOutbDtm"] = ''
    bodyJson["StatEvet"]["statEvetItemCnt"] = 1
    bodyJson["StatEvet"]["statEvetItem"] = statEvetItem
    bodyJson["StatEvet"]["cpxRelEvetOutbSeqnCnt"] = 0
    bodyJson["StatEvet"]["outbPos"] = mrsConfig.location

    sendToErs(bodyJson)
    pass


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