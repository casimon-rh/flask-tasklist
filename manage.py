"""manager"""
import os
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import BD_, create_app


APP = create_app(config_name=os.getenv('APP_SETTINGS'))
MIGRATE = Migrate(APP, BD_)
MANAGER = Manager(APP)

MANAGER.add_command('db', MigrateCommand)


if __name__ == '__main__':
    MANAGER.run()
