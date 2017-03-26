#coding:utf-8
'''系统的所有数据存储在本地mysql数据库中,但是由于mysql数据库很难进行用户的授权登录机制（本人水平有限），
系统使用falsk的第三方扩展flask-login，建立sqlalchemy的数据模型，进行登录登出的维护，
此用户模型仅记录用户的username字段，用于和mysql数据库连接'''

from flask_login import UserMixin
from . import login_manager
from . import db

class User(UserMixin,db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(128),unique=True, index=True)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))