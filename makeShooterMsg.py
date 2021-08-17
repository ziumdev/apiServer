import datetime
import time
from flask import Flask, request
from apiServerConfig import apiConfig, smsCodeConfig


def makeShooterMsg(param):
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

    regimentArr = param['StatEvet']['uSvcOutbId'].split('-')

    regiment = smsCodeConfig.regiment[regimentArr[0]]
    missionType = smsCodeConfig.missionType[regimentArr[2][3:6]]
    status = ''

    location = param['StatEvet']['outbPos']
    eventContent = param['StatEvet']['statEvetNm'] + '이벤트 발생' + ', ' + ''
    groupCode = 'EE-01'

    msg['EventId'] = str(time.time()*1000)
    msg['EventDateTime'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
    msg['Regiment'] = regiment
    msg['MissionType'] = missionType
    # msg['EventRemark'] = {
    #     'coordinate': location,
    #     'EventContent': eventContent
    # }
    msg['GroupCode'] = groupCode


    return msg