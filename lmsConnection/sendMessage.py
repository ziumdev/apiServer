import socket, uuid
from extConfig import mrsConfig, lmsConfig
import datetime, json, struct


def sendMsg(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((mrsConfig.mrsHost, mrsConfig.mrsPort))
    sock.send(msg)
    sock.close()


def makeEventMsg(data):
    print(data)
    statEvetNm = data['obj'] + ' '+ data['kind']

    stdCd = mrsConfig.mrsClientCd + '-' + mrsConfig.mrsSiteCd + '-' + '000' + mrsConfig.lmsDisasterCode
    bodyJson = mrsConfig.bodyJson

    uSvcOutbId = str(uuid.uuid4())[:24]
    statEvetId = stdCd + '001' + 'E' + str(20)

    dataKey = 'eventLogic'
    dataValue = data['eventLogic']
    statEvetItem = [{'key': dataKey, 'value': dataValue}]

    bodyJson["StatEvet"]["statEvetId"] = statEvetId
    bodyJson["StatEvet"]["uSvcOutbId"] = uSvcOutbId
    bodyJson["StatEvet"]["statEvetNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetGdCd"] = str(lmsConfig.eventLevel[data['eventLevel']])
    bodyJson["StatEvet"]["procSt"] = 1
    bodyJson["StatEvet"]["outbPosCnt"] = 1
    bodyJson["StatEvet"]["outbPosNm"] = statEvetNm
    if data['eventMessage'].startswith("NAC 차단"):
        bodyJson["StatEvet"]["statEvetCntn"] = '스마트부대망에 비인가 네트워크가 탐지되었습니다'
    else:
        bodyJson["StatEvet"]["statEvetCntn"] = 'LMS에서 로그확인이 필요합니다'
    # bodyJson["StatEvet"]["statEvetCntn"] = data['eventMessage'] + '발생'
    bodyJson["StatEvet"]["statEvetOutbDtm"] = ''
    bodyJson["StatEvet"]["statEvetItemCnt"] = 1
    bodyJson["StatEvet"]["statEvetItem"] = statEvetItem
    bodyJson["StatEvet"]["cpxRelEvetOutbSeqnCnt"] = 0
    bodyJson["StatEvet"]["outbPos"] = mrsConfig.location
    # bodyJson에 담아 mrs, ers로 보내는 내용

    sendToErs(bodyJson)


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
