import json

from apiServerConfig import apiConfig, smsCodeConfig
import time, datetime, requests, json


def listCallup(param):
    runConfig = apiConfig.TestConfig

    param = param.decode('utf-8')
    param = param.replace('&','')
    print(param)
    paramList = param.split('data%5B%5D=')
    print(paramList)
    msg = {
    }
    # msg['EventId'] = str(time.time()*1000)
    # msg['EventDateTime'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')

    for group in paramList:
        if group == 'dron':
            continue
        if len(group) == 0 :
            continue
        msg['EventId'] = str(int(time.time() * 1000))
        msg['EventDateTime'] = str(datetime.datetime.now())[:-7]
        msg['Regiment'] = smsCodeConfig.regiment['PA1'] # 1대대
        msg['MissionType'] = smsCodeConfig.missionType['경계감시']
        msg['EquipID'] = 'ESE'
        msg['EventType'] = smsCodeConfig.eventType['침입']
        msg['ObjectType'] = 'OBT-05' #현역
        msg['Status'] = smsCodeConfig.status['상황접수']
        msg['ActionStartDate'] = str(datetime.datetime.now())
        msg['ActionEndDate'] = str(datetime.datetime.now())
        msg['ActionContents'] = ''
        msg['ResultContents'] = ''

        msg['GroupCode'] = 'EE-' + group[-2:]
        msg['EventRemark'] = '침입 이벤트 발생, 상황접수'
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
