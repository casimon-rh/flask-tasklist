import os

from app import create_app

CONFIG = os.getenv('APP_SETTINGS')
APP = create_app(CONFIG)

if __name__ == '__main__':
    APP.run()
