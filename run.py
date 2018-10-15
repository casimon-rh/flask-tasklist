import os

from app import create_app

CONFIG = os.getenv('APP_SETTINGS')
APP = create_app(config_name=CONFIG)

if __name__ == '__main__':
    APP.run()
