import datetime
from urllib.parse import unquote
from flask import Flask, request, jsonify
from flask_cors import CORS
from apiServerConfig import apiConfig
import json, requests
import sendMsg, vms, callup, carEntryFn
import mgrs
import lidarEvent


app = Flask(__name__)
CORS(app)
runConfig = apiConfig.TestConfig


@app.route('/sos', methods=['POST'])
def mobile():
    print('sos api is called')
    param = request.get_json()
    if 'EventId' not in param:
        return json.dumps({
            "responseCode": 4000,
            "responseMessage": "bad request"
        })
    elif param['Longitude'] == '' or param['Longitude'] is None or param['Latitude'] == '' or param['Latitude'] is None:
        postMsg = sendMsg.makeNoCoordinateMessage(runConfig, param)
        return json.dumps({
            "responseCode": 4001,
            "responseMessage": "location Infomation is missed"
        })
    else:
        postMsg = sendMsg.makeMessage(runConfig, param)
        postMsgData = json.dumps(postMsg, ensure_ascii=False).encode('utf-8')
#        print(postMsgData)
        try:
            header = {
                'Content-Type': 'application/json; charset=utf-8',
            }
#            response = requests.post(url=runConfig.mobileAPIServerHost+runConfig.mobileAPIServerURL, json=postMsg, headers=header)
#            print(
#                {'response': response}
#            )

            return json.dumps({
                "responseCode": 2000,
                "responseMessage": "success"
            })
        except ConnectionError as connError:
            print(connError)
            return json.dumps({
                "responseCode": 4004,
                "responseMessage": "Connection with Mobile API server"
            })
        finally:
            pass


@app.route('/callUp', methods=['POST'])
def callupList():
    param = request.get_json()
    print(param)
    callup.listCallup(param)
    # postMsgData = json.dumps(postMsg, ensure_ascii=False).encode('utf-8')
    # print(postMsgData)
    # try:
    #     header = {
    #         'Content-type': 'application/json',
    #     }
    #     response = requests.post(url=runConfig.mobileAPIServerHost+runConfig.mobileAPIServerURL,  data=postMsgData, headers=header)
    #     print(
    #         {'response': response}
    #     )
    return json.dumps({
           "responseCode": 2000,
           "responseMessage": "success"
    })
    #
    # except ConnectionError as connError:
    #     print(connError)
    #     return json.dumps({
    #         "responseCode": 4004,
    #         "responseMessage": "Connection with Mobile API server"
    #     })
    #     pass


@app.route('/getCamList', methods=['POST'])
def test():
    param = vms.getVmsList()
    return param

@app.route('/getFenceCctvList', methods=['POST'])
def getGuardCctvList():
    param = vms.getFenceCctvList()
    try:
        return {
            "responseCode": 2000,
            "responseMessage": param
        }
    except Exception as e:
        return {
            "responseCode": 4004,
            "errorMessage": str(e)
        }


@app.route('/getLivingCctvList', methods=['POST'])
def getLivingCctvList():
    param = vms.getLivingCctvList()
    try:
        return {
            "responseCode": 2000,
            "responseMessage": param
        }
    except Exception as e:
        return {
            "responseCode": 4004,
            "errorMessage": str(e)
        }


@app.route('/api/getTimeInfo', methods=['POST'])
def sendTimeInfo():
    now = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    param = request.get_json()
    resultData = {}
    try:
        resultData['result'] = 'S'
        resultData['errCd'] = ''
        resultData['equipId'] = param['equipId']
        resultData['dateTime'] = now
    except Exception as e:
        resultData['result'] = 'E'
        resultData['errCd'] = 'E9999'
    finally:
        print(json.dumps(resultData))
        return json.dumps(resultData)

@app.route('/getCctvListByPage', methods=['POST'])
def getCctvListByPage():
    pageNo = request.get_json()
    print(pageNo)
    param = vms.getCctvListByPage(int(pageNo['pageNo']))
    try:
        return {
            "responseCode": 2000,
            "responseMessage": param
        }
    except Exception as e:
        return {
            "responseCode": 4004,
            "errorMessage": str(e)
        }

@app.route('/agent',  methods=['POST'])
def agent():
    param = request.get_json()
    if 'client_cd' and 'site_cd' not in param:
        return json.dumps({
            "responseCode": 4000,
            "responseMessage": "bad request"
        })
    else:
        print(param)
        callup.listCallup(param)
        return json.dumps({
            "responseCode": 2000,
            "responseMessage": "success"
        })

@app.route('/mgrs', methods=['POST'])
def mrgs():
    param = request.get_json()
    print(param)
    mgrs_object = mgrs.MGRS()
    try:
        coordinate = mgrs_object.toMGRS(latitude=param['latitude'], longitude=param['longitude'])
        result = str(coordinate)[0:3] + " "
        result += str(coordinate)[3:5] + " "
        result += str(coordinate)[5:10] + " "
        result += str(coordinate)[10:] + " "
        print(json.dumps({
            "responseCode":2000,
            "responseMessage":result
            }))
        return json.dumps({
            "responseCode": 2000,
            "responseMessage" : result
        })
    except Exception as e:
        return json.dumps({
            "responseCode": 4004,
            "errorMessage": str(e)
        })

@app.route('/api/carEntry', methods=['POST'])
def carEntry():
    param = request.get_json()
    try:
        header = {
            'Content-type': 'application/json',
            'API-KEY': 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1'
        }
        response = requests.post(url='http://211.9.3.50:40020/api/carEntry' , data=param, headers=header)
        return json.dumps({
            "responseCode": "2000",
            "responseMessage": "success"
        })
    except Exception as e:
        return json.dumps({
            "responseCode": 4004,
            "errorMessage": str(e)
        })

@app.route('/api/FlightInfo', methods=['GET'])
def getDroneInfo():
    res = requests.get(url='http://211.9.2.10:8080/api/FlightInfo')
    if res.status_code==200:
        result = res.json()
        print(result)
        mgrs_object = mgrs.MGRS()
        coordinateParam = result["av_pos"]
        coordinateParam = coordinateParam[1:-1].replace(' ','')
        longitude=coordinateParam.split(',')[0]
        latitude=coordinateParam.split(',')[1]
        tempMgrsCoordinate =  mgrs_object.toMGRS(latitude=latitude, longitude=longitude)
        mgrsCoordinate = str(tempMgrsCoordinate)[0:3] + " "
        mgrsCoordinate += str(tempMgrsCoordinate)[3:5] + " "
        mgrsCoordinate += str(tempMgrsCoordinate)[5:10] + " "
        mgrsCoordinate += str(tempMgrsCoordinate)[10:] + " "
        result['mgrsCoordinate'] = mgrsCoordinate
        print(result)
    return json.dumps(result)


@app.route('/getLidarEvent', methods=['POST'])
def getLidarEvent():
    param = unquote(request.get_data().decode('utf8'))
    param = param.replace('text=', '')
    param = json.loads(param)
    lidarEvent.lidarEventProcess(param)
    return json.dumps({
        "responseCode": "2000",
        "responseMessage": "success"
    })

@app.route('/api/OperateDrone',  methods=['GET'])
def operateDrone():
    param = request.get_json()
    print(param)
    reqData = {
                'cctv_id': str(param['equipId']),
                'cctv_pos': f"[{param['coordx']}, {param['coordy']}]"
            }
    print(reqData)
    dronUrl = 'http://211.9.2.10:8080/api/OperateDrone'
    try:
        header = {
                'Content-Type': "application/json"
        }
        response = requests.post(url=dronUrl, data=reqData, headers=header)
        print(response)
        return json.dumps({
            "responseCode": "2000",
            "responseMessage": "success"
        })
    except Exception as e:
        return json.dumps({
            "responseCode": 4004,
            "errorMessage": str(e)
        })
