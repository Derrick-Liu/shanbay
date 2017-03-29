#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DateField,BooleanField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class SetvaluesForm(FlaskForm):
    words_num=StringField(u'每天背单词数量',validators=[DataRequired()])
    type=SelectField(u'单词范围',choices=[(u'0',u'任意' ),(u'1',u'高中'),( u'2',u'四级'),(u'3',u'六级'),(u'4',u'雅思'),(u'5',u'托福')])
    submit=SubmitField(u'提交')

class NotesForm(FlaskForm):
    body=TextAreaField(u'写笔记',validators=[Length(5,300)])
    submit=SubmitField(u'提交')

class SearchForm(FlaskForm):
    word=StringField(u'单词',validators=[DataRequired()])
    submit=SubmitField(u'查询')

