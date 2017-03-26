#coding:utf-8
from flask_script import Manager,Shell
from app import create_app
import os
from app.models import User
from app import db


app=create_app(os.getenv('SHANBAY_CONFIG') or 'default')
manager=Manager(app)


def make_shell_context():
    return dict(app=app,db=db,User=User)
manager.add_command('shell',Shell(make_context=make_shell_context))


if __name__=='__main__':
    manager.run()
