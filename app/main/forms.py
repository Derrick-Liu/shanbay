#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DateField,BooleanField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class SetvaluesForm(FlaskForm):
    words_num=StringField(u'每天背单词数量',validators=[DataRequired()])
    type=SelectField(u'单词范围',choices=[(u'任意', u'任意'), (u'四级', u'四级'),(u'六级',u'六级'),(u'雅思',u'雅思'),(u'托福',u'托福'),(u'GRE',u'GRE')])
    submit=SubmitField(u'提交')

class NotesForm(FlaskForm):
    body=TextAreaField(u'写笔记',validators=[Length(0,300)])
    submit=SubmitField(u'提交')