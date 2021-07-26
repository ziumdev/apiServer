import datetime, json, struct, socket

eventCnt = 0
eventCode = "E"


def sendMsg(runConfig, msg) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((runConfig.mrsHost, runConfig.mrsPort))
    sock.send(msg)
    sock.close()


def makeMessage(runConfig, param):
    eventCode = "E" + str(param['missionType'][-2:])
    global eventCnt
    uSvcOutbId = runConfig.mrsClientCd + '-' + runConfig.mrsSiteCd + '-' + runConfig.headerTypeCd + 'PHN' + str(eventCnt).zfill(3)
    statEvetId = uSvcOutbId + eventCode
    bodyJson = {"StatEvet" : {
        }
    }
    statEvetNm = ''
    eventStatusNm = ''
    missionType = ''
    print(param['eventType'])

    if param['eventType'] == 'EVT-01':
        statEvetNm = "침입"
    elif param['eventType'] == 'EVT-02':
        statEvetNm = "배회"
    elif param['eventType'] == 'EVT-03':
        statEvetNm = "유기"
    elif param['eventType'] == 'EVT-04':
        statEvetNm = "화재"

    if param['missionType'] == 'MT-01':
        missionType = "경계감시"
    elif param['missionType'] == 'MT-02':
        missionType = "안전재난"
    elif param['missionType'] == 'MT-03':
        missionType = "병력생활"
    elif param['missionType'] == 'MT-04':
        missionType = "무기탄약"
    elif param['missionType'] == 'MT-10':
        missionType = "병력현황"

    if param['eventStatus'] == 'EVS-01':
        eventStatusNm = '상황접수'
    elif param['eventStatus'] == 'EVS-02':
        eventStatusNm = '조치 중'
    elif param['eventStatus'] == 'EVS-03':
        eventStatusNm = '상황종료'
    elif param['eventStatus'] == 'EVS-04':
        eventStatusNm = '기타 상황'

    statEvetItem = [{'key': missionType, 'value': eventStatusNm}]

    bodyJson["StatEvet"]["uSvcOutbId"] = uSvcOutbId
    bodyJson["StatEvet"]["statEvetId"] = statEvetId
    bodyJson["StatEvet"]["statEvetNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetGdCd"] = 10
    bodyJson["StatEvet"]["procSt"] = 1
    bodyJson["StatEvet"]["outbPosCnt"] = 1
    bodyJson["StatEvet"]["outbPosNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetCntn"] = statEvetNm + '이벤트 발생' + ', ' + eventStatusNm
    bodyJson["StatEvet"]["statEvetOutbDtm"] = ''
    bodyJson["StatEvet"]["statEvetItemCnt"] = 1
    bodyJson["StatEvet"]["statEvetItem"] = statEvetItem
    bodyJson["StatEvet"]["cpxRelEvetOutbSeqnCnt"] = 0
    bodyJson["StatEvet"]["outbPos"] = runConfig.location

    print(bodyJson)
    # sendToErs(runConfig, bodyJson)
    eventCnt += 1
    print(eventCnt)

def sendToErs(runConfig, jsonData):
    currentDateTimeString = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    headerA = runConfig.mrsClientCd + '     ' + runConfig.mrsSiteCd + 'A1' + '      ' + runConfig.sendSystemCd + " "
    headerB = runConfig.headerTypeCd + runConfig.traceId + currentDateTimeString
    jsonData['StatEvet']['statEvetOutbDtm'] = currentDateTimeString
    bodyByte = json.dumps(jsonData, ensure_ascii=False).encode('utf-8')  # Json 값을 byte로 변경
    # bodyByte = marshal.dumps(bodyJson)
    bodyLength = struct.pack('<I', bodyByte.__len__())
    header = headerA.encode('utf-8').__add__(bodyLength).__add__(headerB.encode('utf-8'))
    msg = header + bodyByte
    sendMsg(runConfig, msg.decode())
    pass
