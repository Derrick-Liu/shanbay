#coding:utf-8
from . import main
from flask import render_template,redirect,url_for,request,session
import pymysql
from .forms import SetvaluesForm,NotesForm
from flask_login import login_required,current_user
import random
import simplejson

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
        type_id=info.get('english_type')
        if cur.execute('select typename from type where id=%d'%int(type_id)):
            type_name=cur.fetchone().get('typename')
        else:
            type_name=u'任意'
        cur.close()
        conn.commit()
        conn.close()
        return render_template('home_page.html',type_name=type_name,number=info.get('words_num_day'))
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

#显示单词页面
@main.route('/abc',methods=['POST','GET'])
def abc():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='lshi6060660',
        db='shanbay',
        charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    if request.method=='GET' and not request.args.get('id'):
        if not current_user.is_authenticated:
            id=random.randint(1,13000)
            day_num=40
        else:
            cur.execute("select english_type,words_num_day from users where username='%s'" % current_user.username)
            info2=cur.fetchone()
            type=info2.get('english_type')
            day_num=info2.get('words_num_day')
            k=random.randint(1,2000)
            id=k*6+int(type)
        session['day_num'] = day_num
    # 用于区分当前请求是提交表单之后的redirect还是普通的请求
    elif request.args.get('id'):
        id = int(request.args.get('id'))
        day_num=session['day_num']
    else:
        #提交表单的post请求时，id为上个get时的id
        id=session['id']
    session['id']=id

    #从words表中获得单词，出现次数和变化形式
    cur.execute("select word,times,exchange from words where id=%d"%id)
    info=cur.fetchone()
    word=info.get('word')                                    #单词
    times=info.get('times')                                  #出现次数
    exchanges=simplejson.loads(info.get('exchange'))         #字典
    other_form=[]
    for key in exchanges:
        if exchanges[key]:                                    #键值为list
            other_form.append(key+': '+','.join(exchanges[key]))

    #从means表中获得单词意思，结果为多个dict组成的list
    cur.execute("select means from means where wordID=%d" % id)
    means_list=cur.fetchall()
    means=[u.get('means') for u in means_list]

    #维护当前已学习个数
    cur_num = request.args.get('cur_num')
    if cur_num:
        if not request.args.get('id'):
            cur_num=int(cur_num)+1
    else:
        cur_num = 1

    #提交笔记
    form=NotesForm()
    if form.validate_on_submit():
        cur.execute('select id from users where username="%s"'%current_user.username)
        user_id=cur.fetchone().get('id')
        cur.execute('insert notes (body,user_id,word_id) values ("%s",%d,%d)'%(form.body.data,user_id,id))

        cur.close()
        conn.commit()
        conn.close()
        return redirect(url_for('main.abc',id=id,cur_num=cur_num))
    cur.close()
    conn.commit()
    conn.close()

    return render_template('abc.html',form=form,other_forms=other_form,word=word,times=times,means=means,cur_num=cur_num,day_num=day_num)

