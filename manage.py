#!python
"""manager"""
import os
import unittest
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import BD_, create_app


APP = create_app(config_name=os.getenv('APP_SETTINGS'))
MIGRATE = Migrate(APP, BD_)
MANAGER = Manager(APP)

MANAGER.add_command('db', MigrateCommand)


# define command for testing called "test"
# Usage: python manage.py test
@MANAGER.command
def test():
    """Runs the unit test without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    MANAGER.run()
