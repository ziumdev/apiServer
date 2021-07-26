from flask import Flask, request, Response, jsonify
from apiServerConfig import apiConfig
import json
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
        sendMsg.makeMessage(runConfig, param)
        return json.dumps({
            "responseCode": 200,
            "responseMessage": "success"
        })


@app.route('/test', methods=['POST'])
def test():
    param = request.get_json()
    print(param)
    return jsonify(param)