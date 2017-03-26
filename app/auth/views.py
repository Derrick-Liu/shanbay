#coding:utf-8
from . import auth
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
import pymysql
from ..models import User
from .. import db


@auth.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='lshi6060660',
            db='shanbay',
            charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

        #在cmd命令行，where后username不存在时返回0，不报错，但不知为何在脚本文件中会报错，这里用try...except...语句处理错误
        try:
            num=cur.execute('select password_hash from users where username=%s'%form.username.data)
            psd_hash=cur.fetchone()
            if num and check_password_hash(psd_hash,form.password.data):       #登录条件仍然依赖mysql数据，check_password_hash()验证密码

                user=User.query.filter_by(username=form.username.data).first()  #User模型用于用户登入
                login_user(user,form.remember_me)

                return redirect(url_for('main.home'))
        except:
            flash(u'用户名或密码无效！')

        cur.close()
        conn.commit()
        conn.close()
    return render_template('auth/login.html',form=form)


@auth.route('register',methods=['POST','GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        # 存储密码的散列值，增加数据安全性
        password_hash=generate_password_hash(form.password.data)
        # 将用户注册数据写入mysql数据库
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='lshi6060660',
            db='shanbay',
            charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        info = (form.email.data,
                form.username.data,
                form.english_type.data,
                password_hash,
                form.gender.data,
                form.birthday.data,
                form.address.data,
                form.about_me.data
                )
        Insert_info = "INSERT users (email,username,english_type,password_hash,gender,birthday,address,about_me) " \
                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(Insert_info, info)
        cur.close()
        conn.commit()
        conn.close()

        #同时将用户名写入models的User模型中，与mysql数据同步
        user=User(
            username=form.username.data
        )
        db.session.add(user)

        flash(u'您现在可以登录！')
        return redirect(url_for('.login'))
    return render_template('auth/register.html',form=form)


