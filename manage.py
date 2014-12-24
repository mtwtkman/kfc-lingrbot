# -*- coding: utf-8 -*-

from app import app, db, KFC
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
  return dict(app=app, db=db, KFC=KFC)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()
