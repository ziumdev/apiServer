from apiServerConfig import apiConfig, smsCodeConfig
import time, datetime, requests


def listCallup(param):
    runConfig = apiConfig.TestConfig

    msg = {
        'EventId': '',
        'EventDateTime': '',
        'Regiment': '',
        'MissionType': '',
        'EquipID': '',
        'EventType': '',
        'ObjectType': '',
        'Status': '',
        'ActionStartDate': '',
        'ActionEndDate': '',
        'ActionContents': '',
        'ResultContents': '',
        'GroupCode': '',
        'EventRemark': '',
        'IsSendOk': 'N'
    }

    # msg['EventId'] = str(time.time()*1000)
    # msg['EventDateTime'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')

    for group in param:
        msg['EventId'] = str(time.time() * 1000)
        msg['EventDateTime'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg['Regiment'] = smsCodeConfig.regiment['PA1'] # 1대대
        msg['MissionType'] = smsCodeConfig.missionType['경계감시']
        msg['EquipID'] = 'ESE'
        msg['EventType'] = smsCodeConfig.missionType['침입']
        msg['ObjectType'] = 'OBT-05' #현역
        msg['Status'] = smsCodeConfig.status['상황접수']
        msg['ActionStartDate'] = str(datetime.datetime.now())
        msg['ActionEndDate'] = str(datetime.datetime.now())
        msg['ActionContents'] = ''
        msg['ResultContents'] = ''

        msg['GroupCode'] = group
        msg['EventRemark'] = '침입 이벤트 발생, 상황접수'

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