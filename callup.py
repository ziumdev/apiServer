from apiServerConfig import apiConfig, smsCodeConfig
import time, datetime, requests, json


def listCallup(param):
    runConfig = apiConfig.TestConfig
    # param = json.loads(param)
    siteCd = str(param['site_cd']) # 부대코드 PA1

    # 전파대상이 리스트인시 스트링인지 체크
    targetList = []
    if type(param['target']) is list:
        targetList.extend(param['target']) # 전파대상
    elif type(param['target']) is str:
        targetList.append(param['target'])
    eventMessage = param['stat_evet_cntn']
    svcThemeCd = param['svc_theme_cd']
    statEvetCd = str(param['stat_evet_cd'])
    eventType = str(svcThemeCd+statEvetCd)
    statEvetOutbSeqn = str(param['stat_evet_outb_seqn'])

    msg = {
    }

    for target in targetList:
        print(target)
        if target == 'dron':
            continue
        if len(target) == 0 :
            continue
        msg['EventId'] = str(int(time.time() * 1000))
        msg['EventDateTime'] = str(datetime.datetime.now())[:-7]
        msg['Regiment'] = smsCodeConfig.regiment[siteCd]
        msg['MissionType'] = smsCodeConfig.missionType[svcThemeCd]
        msg['EquipID'] = param['equipId']
        msg['EventType'] = smsCodeConfig.eventType[eventType]
        if svcThemeCd == 'PHN':
            if eventType == 'PHN10':
                msg['EventType'] = 'MT-11'
            else:
                msg['EventType'] = 'MT-03'
        msg['ObjectType'] = smsCodeConfig.regiment[siteCd]#현역
        msg['Status'] = smsCodeConfig.status['상황접수']
        msg['ActionStartDate'] = str(datetime.datetime.now())
        msg['ActionEndDate'] = str(datetime.datetime.now())
        msg['ActionContents'] = ''
        msg['ResultContents'] = ''

        msg['GroupCode'] = target
        msg['EventRemark'] = eventMessage
        msg['IsSendOk'] = 'N'

        msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
        print(msg)
        try:
            header = {
                'Content-type': 'application/json'
            }
            response = requests.post(url=runConfig.mobileAPIServerHost+runConfig.mobileAPIServerURL,  data=msg, headers=header)
            print(
                {'response': response}
            )
        except Exception as e:
            print(e)
            continue
        finally:
            msg = {}

