#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DateField,BooleanField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class RegisterForm(FlaskForm):
    email=StringField(u'邮箱 *',validators=[DataRequired(),Email(),Length(1,64)])
    username=StringField(u'用户名 *',validators=[DataRequired(),Length(6,20)])
    password=PasswordField(u'密码 *',validators=[DataRequired(),Length(6,30),EqualTo('password2',message=u'密码必须匹配')])
    password2=PasswordField(u'确认密码 *',validators=[DataRequired()])
    english_type=SelectField(u'英语等级 *',validators=[DataRequired()],choices=[(1,u'任意'),(2,u'高中'),(3,u'四级'),(4,u'六级'),(5,u'雅思'),(6,u'托福')])
    gender=SelectField(u'性别',choices=[(1,u'男'),(2,u'女',)])
    birthday=DateField(u'出生日期')
    address=StringField(u'地址',validators=[Length(20)])
    about_me=TextAreaField(u'自我介绍',validators=[Length(200)])
    submit=SubmitField(u'提交')

class LoginForm(FlaskForm):
    username=StringField(u'用户名',validators=[DataRequired()])
    password=PasswordField(u'密码',validators=[DataRequired()])
    remember_me=BooleanField(u'记住密码？')
    submit=SubmitField(u'登录')

