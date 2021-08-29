import json

from apiServerConfig import apiConfig, smsCodeConfig
import time, datetime, requests, json


def listCallup(param):
    runConfig = apiConfig.TestConfig

    siteCd = param['site_cd'] # 부대코드 PA1
    targetList = param['target'] # 전파대상
    eventMessage = param['stat_evet_cntn']
    svcThemeCd = param['svc_theme_cd']
    statEvetCd = str(param['stat_evet_cd'])
    eventType = str(svcThemeCd+statEvetCd)
    # param = param.decode('utf-8')
    # param = param.replace('&','')
    # paramList = param.split('data%5B%5D=')

    msg = {
    }
    # msg['EventId'] = str(time.time()*1000)
    # msg['EventDateTime'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')

    for target in targetList:
        if target == 'dron':
            continue
        if len(target) == 0 :
            continue
        msg['EventId'] = str(int(time.time() * 1000))
        msg['EventDateTime'] = str(datetime.datetime.now())[:-7]
        msg['Regiment'] = smsCodeConfig.regiment[siteCd] # 1대대
        msg['MissionType'] = smsCodeConfig.missionType[svcThemeCd]
        msg['EquipID'] = 'ESE'
        msg['EventType'] = smsCodeConfig.eventType[eventType]
        msg['ObjectType'] = 'OBT-05' #현역
        msg['Status'] = smsCodeConfig.status['상황접수']
        msg['ActionStartDate'] = str(datetime.datetime.now())
        msg['ActionEndDate'] = str(datetime.datetime.now())
        msg['ActionContents'] = ''
        msg['ResultContents'] = ''

        # msg['GroupCode'] = 'EE-' + group[-2:] 타켓리스트에 대한 코드가 들어가야함
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
