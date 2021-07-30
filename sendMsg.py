import datetime, json, struct, socket
import uuid
eventCnt = '10'
eventCode = "E"


def sendMsg(runConfig, msg) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((runConfig.mrsHost, runConfig.mrsPort))
    sock.send(msg)
    sock.close()


def makeMessage(runConfig, param):
    eventCode = "E" + str(param['MissionType'][-2:])
    global eventCnt
    uSvcOutbId = str(uuid.uuid4())[0:24]
    statEvetId = runConfig.mrsClientCd + '-' + runConfig.mrsSiteCd + '-' + '000' + 'PHN' + '010' + eventCode
    bodyJson = {"StatEvet": {
        }
    }
    statEvetNm = ''
    eventStatusNm = ''
    missionType = ''
    groupCode = ''

    if param['EventType'] == 'EVT-01':
        statEvetNm = "침입"
    elif param['EventType'] == 'EVT-02':
        statEvetNm = "배회"
    elif param['EventType'] == 'EVT-03':
        statEvetNm = "유기"
    elif param['EventType'] == 'EVT-04':
        statEvetNm = "화재"

    if param['MissionType'] == 'MT-01':
        missionType = "경계감시"
        groupCode = 'EE-01'
    elif param['MissionType'] == 'MT-02':
        missionType = "안전재난"
        groupCode = 'EE-02'
    elif param['MissionType'] == 'MT-03':
        missionType = "병력생활"
        groupCode = 'EE-03'
    elif param['MissionType'] == 'MT-04':
        missionType = "무기탄약"
        groupCode = 'EE-03'
    elif param['MissionType'] == 'MT-10':
        missionType = "병력현황"
        groupCode = 'EE-01'

    if param['Status'] == 'EVS-01':
        eventStatusNm = '상황접수'
    elif param['Status'] == 'EVS-02':
        eventStatusNm = '조치 중'
    elif param['Status'] == 'EVS-03':
        eventStatusNm = '상황종료'
    elif param['Status'] == 'EVS-04':
        eventStatusNm = '기타 상황'

    statEvetItem = [
        {'key': missionType, 'value': eventStatusNm},
        {'key': 'data', 'value': param},
        {'key': 'groupCode', 'value': 'EE-01'}
    ]

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

    print("ERS msg")
    print(bodyJson)
    sendToErs(runConfig, bodyJson)

    param['EquipID'] = 'ESE'
    param['EventRemark'] = statEvetNm + '이벤트 발생' + ', ' + missionType + ' ' + eventStatusNm
    param['EventDateTime'] = str(datetime.datetime.now())
    param['GroupCode'] = groupCode
    param['IsSendOk'] = 'N'
    print('mobile Shooter Msg check')

    return param


def sendToErs(runConfig, jsonData):
    currentDateTimeString = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    headerA = runConfig.mrsClientCd + '     ' + runConfig.mrsSiteCd + 'A1' + '      ' + runConfig.sendSystemCd + " "
    headerB = runConfig.headerTypeCd + runConfig.traceId + currentDateTimeString
    jsonData['StatEvet']['statEvetOutbDtm'] = currentDateTimeString
    bodyByte = json.dumps(jsonData, ensure_ascii=False).encode('utf-8')  # Json 값을 byte로 변경
    bodyLength = struct.pack('<I', bodyByte.__len__())
    header = headerA.encode('utf-8').__add__(bodyLength).__add__(headerB.encode('utf-8'))
    msg = header + bodyByte
    sendMsg(runConfig, msg)
    pass
