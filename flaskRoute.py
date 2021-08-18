import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from apiServerConfig import apiConfig
import json, requests
import sendMsg, vms, callup
import mgrs


app = Flask(__name__)
CORS(app)
runConfig = apiConfig.TestConfig


@app.route('/sos', methods=['POST'])
def mobile():
    param = request.get_json()
    if 'EventId' not in param:
        return json.dumps({
            "responseCode": 4000,
            "responseMessage": "bad request"
        })
    else:
        postMsg = sendMsg.makeMessage(runConfig, param)
        postMsgData = json.dumps(postMsg, ensure_ascii=False).encode('utf-8')
        print(postMsgData)
        try:
            header = {
                'Content-type': 'application/json',
            }
            response = requests.post(url=runConfig.mobileAPIServerHost+runConfig.mobileAPIServerURL,  data=postMsgData, headers=header)
            print(
                {'response': response}
            )

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
    param = request.get_data()
    print(param)
    postMsg = callup.listCallup(param)
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
    #     return json.dumps({
    #         "responseCode": 2000,
    #         "responseMessage": "success"
    #     })
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


@app.route('/api/getTimeInfo', methods=['POST'])
def sendTimeInfo():
    now = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')[:-3]
    param = request.get_json()
    resultData = {}
    try:
        resultData['result'] = 'S'
        resultData['errCd'] = ''
        resultData['equipId'] = param['equipId']
        resultData['DateTime'] = now
    except Exception as e:
        resultData['result'] = 'E'
        resultData['errCd'] = 'E9999'
    finally:
        return json.dumps(resultData)


@app.route('/agent',  methods=['POST'])
def agent():
    param = request.get_json()
    if 'EventId' not in param:
        return json.dumps({
            "responseCode": 4000,
            "responseMessage": "bad request"
        })
    else:
        postMsg = sendMsg.makeMessage(runConfig, param)
        postMsgData = json.dumps(postMsg, ensure_ascii=False).encode('utf-8')
        print(postMsgData)
        try:
            header = {
                'Content-type': 'application/json',
            }
            response = requests.post(url=runConfig.mobileAPIServerHost+runConfig.mobileAPIServerURL,  data=postMsgData, headers=header)
            print(
                {'response': response}
            )

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


@app.route('/mgrs', methods=['POST'])
def mrgs():
    param = request.get_json()
    mgrs_object = mgrs.MGRS()
    try:
        coordinate = mgrs_object.toMGRS(latitude=param['latitude'], longitude=param['longitude'])
        result = str(coordinate)[0:3] + " "
        result += str(coordinate)[3:5] + " "
        result += str(coordinate)[5:10] + " "
        result += str(coordinate)[10:] + " "
        return json.dumps({
            "responseCode": 2000,
            "responseMessgae" : result
        })
    except Exception as e:
        return json.dumps({
            "responseCode": 4004,
            "errorMessage": str(e)
        })