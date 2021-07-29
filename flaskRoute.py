from flask import Flask, request, jsonify
from apiServerConfig import apiConfig
import json, requests
import sendMsg

app = Flask(__name__)
runConfig = apiConfig.TestConfig


@app.route('/sos', methods=['POST'])
def mobile():
    param = request.get_json()
    if 'EventId' not in param :
        return json.dumps({
            "responseCode": 4000,
            "responseMessage": "bad request"
        })
    else:
        postMsg = sendMsg.makeMessage(runConfig, param)
        try:
            requests.post(url=runConfig.mobileAPIServerHost+runConfig.mobileAPIServerURL, data=json.dumps(postMsg))
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


@app.route('/test', methods=['POST'])
def test():
    param = request.get_json()
    print(param)
    return jsonify(param)