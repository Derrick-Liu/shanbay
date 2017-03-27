#coding:utf-8
from . import main
from flask import render_template,redirect,url_for,request
import pymysql
from .forms import SetvaluesForm,NotesForm
from flask_login import login_required,current_user

#主页
@main.route('/')
def home():
    if current_user.is_authenticated:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='lshi6060660',
            db='shanbay',
            charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cur.execute('select english_type,words_num_day from users where username="%s"'%current_user.username)
        info=cur.fetchone()   #获取已登录用户的单词类型和每日背单词数，传入模板，在主页显示

        cur.close()
        conn.commit()
        conn.close()
        return render_template('home_page.html',type=info.get('english_type'),number=info.get('words_num_day'))
    return render_template('home_page.html')

#设置用户单词类型和每日背单词数量
@main.route('/set_value/<username>',methods=["POST","GET"])
@login_required
def set_value(username):
    form=SetvaluesForm()
    if form.validate_on_submit():
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='lshi6060660',
            db='shanbay',
            charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

        cur.execute("update users set english_type='%s',words_num_day='%s' where username='%s'"%(form.type.data,form.words_num.data,username))

        cur.close()
        conn.commit()
        conn.close()
        return redirect(url_for('main.home'))
    return render_template('set_values.html',form=form)

#显示单词页面，单词id为参数
@main.route('/abc/<int:id>',methods=['POST','GET'])
@login_required
def abc(id):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='lshi6060660',
        db='shanbay',
        charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    form=NotesForm()
    #从words表中获得单词，出现次数和变化形式
    cur.execute("select word,times,exchange from words where id=%d"%id)
    info=cur.fetchone()
    word=info.get('word')
    times=info.get('times')
    exchanges=info.get('exchange')          #字典

    #从means表中获得单词意思，结果为多个dict组成的list
    cur.execute("select means from means where wordID=%d" % id)
    means_list=cur.fetchall()
    means=[u.get('means') for u in means_list]

    if form.validate_on_submit():
        cur.execute('select id from users where username="%s"'%current_user.username)
        user_id=cur.fetchone().get('id')
        cur.execute('insert notes (body,user_id,word_id) values (%s,%d,%d)'%(form.body.data,user_id,id))

        cur.close()
        conn.commit()
        conn.close()
        return redirect(url_for('main.abc',id=id))
    cur.close()
    conn.commit()
    conn.close()

    return render_template('abc.html',form=form,word=word,times=times,means=means)

