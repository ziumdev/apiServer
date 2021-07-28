from flask import Flask, request, jsonify
from apiServerConfig import apiConfig
import json, requests
import sendMsg

app = Flask(__name__)
runConfig = apiConfig.TestConfig


@app.route('/sos', methods=['POST'])
def mobile():
    param = request.get_json()
    if 'eventId' not in param :
        return json.dumps({
            "responseCode": 400,
            "responseMessage": "bad request"
        })
    else:
        postMsg = sendMsg.makeMessage(runConfig, param)
        requests.post(url='110.10.130.51:5002/Emergency/EventStatus/EventStatusSave', data=json.dumps(postMsg))
        return json.dumps({
            "responseCode": 200,
            "responseMessage": "success"
        })


@app.route('/test', methods=['POST'])
def test():
    param = request.get_json()
    print(param)
    return jsonify(param)