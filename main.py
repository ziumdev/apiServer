import sys
from apiServerConfig import apiConfig
from flask_apscheduler import APScheduler
import flaskRoute
from lmsConnection import connection as lmsConn

def create_app(config_name):
    app = flaskRoute.app
    app.config.from_object(apiConfig.config_by_name[config_name])
    return app


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.add_job(id='check LMS', func=lmsConn.run, trigger='interval', second=1)

    env = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    # create_app(env).run(host='localhost', port=49999)
    create_app(env).run(host='0.0.0.0', port=49999)
    # create_app(env).run(host=apiConfig.TestConfig.serverHost, port=apiConfig.TestConfig.serverPort)
