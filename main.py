import sys
from flask import Flask
from apiServerConfig import apiConfig
import flaskRoute


def create_app(config_name):
    app = flaskRoute.app
    app.config.from_object(apiConfig.config_by_name[config_name])
    return app


if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    create_app(env).run(port=49999)
