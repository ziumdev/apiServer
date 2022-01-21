import datetime, json, struct, socket
import uuid
eventCnt = '10'
eventCode = "E"


def sendMsg(runConfig, msg) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((runConfig.mrsHost, runConfig.mrsPort))
    sock.send(msg)
    sock.close()

'''
'''

def makeMessage(runConfig, param):
    print(param)
    regimCompany = param['RegimCompany']        # 중대
    rank = param['Rank']                        # 사용자 계급
    personName = param['Name']                  # 사용자 이름
    equipId = param['EquipID']                  # 장비 번호
#    latitude = param['Latitude']                # 위도
#    longitude = param['Longitude']              # 경도
#    altitude = param['Altitude']
    isDevice = param['IsDevice']                # 워치, 비콘 여부 결정
    roomName = param['RoomName']                # 비콘일 시, 비콘의 건물명
    roomNumber = param['RoomNumber']            # 비콘일 시, 비콘의 장소넘버
    equipLocation = param['EquipLocation']      # 비콘일 시, 비콘의 장소이름
    userKey = param['UseyKey']

    latitude = ''
    if param['Latitude'] == None:
        latitude = 0            # 위도
    elif param['Latitude'] != None:
        latitude = param['Latitude']

    longitude = ''

    if param['Longitude'] == None:
        longitude = 0
    elif param['Longitude'] != None:
        longitude = param['Longitude']          #경도
#    longitude = param['Longitude']
#    altitude = param['Altitude']


    eventCode = "E" + str(param['MissionType'][-2:])
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
        groupCode = 'BN51'
    elif param['EventType'] == 'EVT-02':
        statEvetNm = "배회"
        groupCode = 'BN51'
    elif param['EventType'] == 'EVT-03':
        statEvetNm = "유기"
        groupCode = 'BN51'
    elif param['EventType'] == 'EVT-04':
        statEvetNm = "화재"
        groupCode = 'BN61'
    elif param['EventType'] == 'EVT-16':
        statEvetNm = "긴급 SOS"
        groupCode = 'BNZZ'
        param['MissionType'] = 'MT-10'

    if param['MissionType'] == 'MT-01':
        missionType = "경계감시"
        # groupCode = 'EE-01'
    elif param['MissionType'] == 'MT-02':
        missionType = "안전재난"
        # groupCode = 'EE-02'
    elif param['MissionType'] == 'MT-03':
        missionType = "병력생활"
        # groupCode = 'EE-03'
    elif param['MissionType'] == 'MT-04':
        missionType = "무기탄약"
        # groupCode = 'EE-03'
    elif param['MissionType'] == 'MT-10':
        missionType = "병력현황"
        # groupCode = 'EE-01'

    if param['Status'] == 'EVS-01':
        eventStatusNm = '상황접수'
    elif param['Status'] == 'EVS-02':
        eventStatusNm = '조치 중'
    elif param['Status'] == 'EVS-03':
        eventStatusNm = '상황종료'
    elif param['Status'] == 'EVS-04':
        eventStatusNm = '기타 상황'

    statEvetItem = [
            {'key':'coordx', 'value':longitude},
            {'key':'coordy', 'value':latitude},
            {'key':'equipId', 'value':equipId},
            {'key':'userKey', 'value':userKey}
    ]

    eventMsg = ''
    if isDevice == 'W-B':    # 비콘일때
        # eventMsg = regimCompany + ' ' + personName + ' ' + rank + ' ' + roomName + ' ' + equipLocation + '에서 SOS 호출'
        eventMsg = regimCompany + ' ' + personName + ' ' + rank + ' ' + roomName + ' ' + '에서 SOS 호출'
        pass
    elif isDevice == 'W-G':  # P-LTE 일 때
        eventMsg = regimCompany[3:] + ' ' + personName + ' ' + rank + ' ' + 'SOS 호출'
    else:
        eventMsg = regimCompany[3:] + ' ' + personName + ' ' + rank + ' ' + 'SOS 호출'
        pass

    bodyJson["StatEvet"]["uSvcOutbId"] = uSvcOutbId
    bodyJson["StatEvet"]["statEvetId"] = statEvetId
    bodyJson["StatEvet"]["statEvetNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetGdCd"] = 10
    bodyJson["StatEvet"]["procSt"] = 1
    bodyJson["StatEvet"]["outbPosCnt"] = 1
    bodyJson["StatEvet"]["outbPosNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetCntn"] = eventMsg
    bodyJson["StatEvet"]["statEvetOutbDtm"] = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    bodyJson["StatEvet"]["statEvetItemCnt"] = 1
    bodyJson["StatEvet"]["statEvetItem"] = statEvetItem
    bodyJson["StatEvet"]["cpxRelEvetOutbSeqnCnt"] = 0
    location = [{
        'y': latitude,
        'x': longitude,
        'z': 0
    }]
    bodyJson["StatEvet"]["outbPos"] = location

    print("ERS msg")
    print(bodyJson)
    sendToErs(runConfig, bodyJson)

    param['EventRemark'] = statEvetNm + '이벤트 발생' + ', ' + missionType + ' ' + eventStatusNm
    param['EventDateTime'] = str(datetime.datetime.now())
    param['ActionStartDate'] = str(datetime.datetime.now())
    param['GroupCode'] = groupCode
    param['IsSendOk'] = 'N'
    print('mobile Shooter Msg check')

    return param


def makeNoCoordinateMessage(runConfig, param):
    print(param)
    regimCompany = param['RegimCompany']        # 중대
    rank = param['Rank']                        # 사용자 계급
    personName = param['Name']                  # 사용자 이름
    equipId = param['EquipID']                  # 장비 번호
#    latitude = param['Latitude']                # 위도
#    longitude = param['Longitude']              # 경도
#    altitude = param['Altitude']
    isDevice = param['IsDevice']                # 워치, 비콘 여부 결정
    roomName = param['RoomName']                # 비콘일 시, 비콘의 건물명
    roomNumber = param['RoomNumber']            # 비콘일 시, 비콘의 장소넘버
    equipLocation = param['EquipLocation']      # 비콘일 시, 비콘의 장소이름
    userKey = param['UseyKey']

    # 기본좌표 추가
    location = runConfig.location
    coordx = location[0]['x']
    coordy = location[0]['y']

    eventCode = "E" + str(param['MissionType'][-2:])
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
        groupCode = 'BN51'
    elif param['EventType'] == 'EVT-02':
        statEvetNm = "배회"
        groupCode = 'BN51'
    elif param['EventType'] == 'EVT-03':
        statEvetNm = "유기"
        groupCode = 'BN51'
    elif param['EventType'] == 'EVT-04':
        statEvetNm = "화재"
        groupCode = 'BN61'
    elif param['EventType'] == 'EVT-16':
        statEvetNm = "긴급 SOS"
        groupCode = 'BNZZ'
        param['MissionType'] = 'MT-10'

    if param['MissionType'] == 'MT-01':
        missionType = "경계감시"
        # groupCode = 'EE-01'
    elif param['MissionType'] == 'MT-02':
        missionType = "안전재난"
        # groupCode = 'EE-02'
    elif param['MissionType'] == 'MT-03':
        missionType = "병력생활"
        # groupCode = 'EE-03'
    elif param['MissionType'] == 'MT-04':
        missionType = "무기탄약"
        # groupCode = 'EE-03'
    elif param['MissionType'] == 'MT-10':
        missionType = "병력현황"
        # groupCode = 'EE-01'

    if param['Status'] == 'EVS-01':
        eventStatusNm = '상황접수'
    elif param['Status'] == 'EVS-02':
        eventStatusNm = '조치 중'
    elif param['Status'] == 'EVS-03':
        eventStatusNm = '상황종료'
    elif param['Status'] == 'EVS-04':
        eventStatusNm = '기타 상황'

    statEvetItem = [
            {'key':'coordx', 'value':coordx},
            {'key':'coordy', 'value':coordy},
            {'key':'equipId', 'value':equipId},
            {'key':'userKey', 'value':userKey}
    ]

    eventMsg = ''
    if isDevice == 'W-B':    # 비콘일때
        # eventMsg = regimCompany + ' ' + personName + ' ' + rank + ' ' + roomName + ' ' + equipLocation + '에서 SOS 호출'
        eventMsg = regimCompany + ' ' + personName + ' ' + rank + ' ' + roomName + ' ' + '에서 SOS 호출'
        pass
    elif isDevice == 'W-G':  # P-LTE 일 때
        eventMsg = regimCompany[3:] + ' ' + personName + ' ' + rank + ' ' + 'SOS 호출 (위치확인불가)'
    else:
        eventMsg = regimCompany[3:] + ' ' + personName + ' ' + rank + ' ' + 'SOS 호출 (위치확인불가)'
        pass

    bodyJson["StatEvet"]["uSvcOutbId"] = uSvcOutbId
    bodyJson["StatEvet"]["statEvetId"] = statEvetId
    bodyJson["StatEvet"]["statEvetNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetGdCd"] = 10
    bodyJson["StatEvet"]["procSt"] = 1
    bodyJson["StatEvet"]["outbPosCnt"] = 1
    bodyJson["StatEvet"]["outbPosNm"] = statEvetNm
    bodyJson["StatEvet"]["statEvetCntn"] = eventMsg
    bodyJson["StatEvet"]["statEvetOutbDtm"] = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    bodyJson["StatEvet"]["statEvetItemCnt"] = 1
    bodyJson["StatEvet"]["statEvetItem"] = statEvetItem
    bodyJson["StatEvet"]["cpxRelEvetOutbSeqnCnt"] = 0
    # 기본좌표 추가
    bodyJson["StatEvet"]["outbPos"] = location

    print("ERS msg")
    print(bodyJson)
    sendToErs(runConfig, bodyJson)

    param['EventRemark'] = statEvetNm + '이벤트 발생' + ', ' + missionType + ' ' + eventStatusNm
    param['EventDateTime'] = str(datetime.datetime.now())
    param['ActionStartDate'] = str(datetime.datetime.now())
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

