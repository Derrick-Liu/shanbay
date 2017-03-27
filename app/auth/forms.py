#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class RegisterForm(FlaskForm):
    email=StringField(u'邮箱 *',validators=[DataRequired(),Email(),Length(1,64)])
    username=StringField(u'用户名 *',validators=[DataRequired(),Length(3,20)])
    password=PasswordField(u'密码 *',validators=[DataRequired(),Length(3,30),EqualTo('password2',message=u'密码必须匹配')])
    password2=PasswordField(u'确认密码 *',validators=[DataRequired()])
    english_type=SelectField(u'英语等级 *',validators=[DataRequired()],choices=[(u'任意',u'任意'),(u'高中',u'高中'),(u'四级',u'四级'),(u'六级',u'六级'),(u'雅思',u'雅思'),(u'托福',u'托福')])
    gender=SelectField(u'性别',choices=[(u'男',u'男'),(u'女',u'女')])
    birthday=StringField(u'出生日期')
    address=StringField(u'地址',validators=[Length(0,20)])
    about_me=TextAreaField(u'自我介绍',validators=[Length(0,200)])
    submit=SubmitField(u'提交')

class LoginForm(FlaskForm):
    username=StringField(u'用户名',validators=[DataRequired()])
    password=PasswordField(u'密码',validators=[DataRequired()])
    remember_me=BooleanField(u'记住密码？')
    submit=SubmitField(u'登录')

