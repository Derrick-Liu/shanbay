#coding:utf-8
from . import main
from flask import render_template,redirect,url_for,request,session,make_response
import pymysql
from .forms import SetvaluesForm,NotesForm,SearchForm
from flask_login import login_required,current_user
import random
import simplejson

#主页
@main.route('/',methods=["POST","GET"])
def home():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='lshi6060660',
        db='shanbay',
        charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    form=SearchForm()
    if request.method=="POST":
        if form.validate_on_submit():
            cur.execute('select id from words where word="%s"'%form.word.data)
            id=int(cur.fetchone().get('id'))

            cur.close()
            conn.commit()
            conn.close()
            return redirect(url_for('main.abc',id=id,search=1))

    show_mine = bool(request.cookies.get('show_mine',''))

    #当不是show_mine的时候才执行获取所有笔记，如果show_mine已经为true，直接执行下面获取个人笔记即可
    if not show_mine:
        #获得所有笔记列表
        cur.execute('select body,time,user_id,word_id,agree_num from notes order by time desc')
        notes_list=cur.fetchall()
        for i in range(len(notes_list)):
            note=notes_list[i]    #多个字段的字典
            #把id转换成name
            cur.execute('select username from users where id=%d'%int(note.get('user_id')))
            user_name =cur.fetchone().get('username')
            cur.execute('select word from words where id=%d' % int(note.get('word_id')))
            word_name = cur.fetchone().get('word')

            list1=[user_name,word_name,note.get('body'),note.get('agree_num'),note.get('time')]
            notes_list[i]=list1

    if current_user.is_authenticated:
        if show_mine:
            cur.execute('select id from users where username="%s"'%current_user.username)
            user_id=int(cur.fetchone().get('id'))
            cur.execute('select body,time,word_id,agree_num from notes where user_id=%d order by time desc'%user_id)
            notes_list = cur.fetchall()
            for i in range(len(notes_list)):
                note = notes_list[i]  # 多个字段的字典
                # 把id转换成name
                cur.execute('select word from words where id=%d' % int(note.get('word_id')))
                word_name = cur.fetchone().get('word')

                list2 = [current_user.username,word_name,note.get('body'),note.get('agree_num'),note.get('time')]
                notes_list[i] =list2
        cur.execute('select english_type,words_num_day from users where username="%s"'%current_user.username)
        info=cur.fetchone()   #获取已登录用户的单词类型和每日背单词数，传入模板，在主页显示
        type_id=info.get('english_type')
        #英语等级中有1,2,3,4,5分别对应高中，四级，六级，雅思，托福，用户英语默认等级为0（任意），表示不等级，范围为所有单词
        if cur.execute('select typename from type where id=%d'%int(type_id)):
            type_name=cur.fetchone().get('typename')
        else:
            type_name=u'任意'
        number = info.get('words_num_day')
    else:
        type_name=u'任意'
        number=40
    cur.close()
    conn.commit()
    conn.close()
    return render_template('home_page.html',form=form,type_name=type_name, number=number, show_mine=show_mine,notes_list=notes_list)

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
        day_num =session.get('day_num', '')
    #提交表单的post请求时，id为上个get时的id
    else:
        id=session['id']
        #当post请求且validate_on_submit() 为False 时用到
        day_num = session.get('day_num', '')
    session['id']=id
    #从words表中获得单词，出现次数和变化形式
    cur.execute("select word,times,exchange from words where id=%d"%id)
    info=cur.fetchone()
    word=info.get('word')                                    #单词
    times=info.get('times')                                  #出现次数
    exchanges=simplejson.loads(info.get('exchange'))         #变化形式，字典
    other_form=[]
    for key in exchanges:
        if exchanges[key]:                                    #键值为list
            other_form.append(key+': '+','.join(exchanges[key]))

    #从means表中获得单词意思，结果为多个dict组成的list
    cur.execute("select means from means where wordID=%d" % id)
    means_list=cur.fetchall()
    means=[u.get('means') for u in means_list]

    #获取当前单词 点赞数前10的笔记内容
    cur.execute('select body,time,user_id,word_id,agree_num from notes where word_id=%d order by agree_num desc' % id)
    notes_list = cur.fetchmany(10)
    for i in range(len(notes_list)):
        note = notes_list[i]
        cur.execute('select username from users where id=%d' % int(note.get('user_id')))
        user_name = cur.fetchone().get('username')
        cur.execute('select word from words where id=%d' % int(note.get('word_id')))
        word_name = cur.fetchone().get('word')
        list2 = [user_name, word_name, note.get('body'), note.get('agree_num'), note.get('time')]
        notes_list[i] = list2

    #维护当前已学习个数,用于显示进度条
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

    #如是查词请求，不渲染下一个按钮和进度条
    search=bool(request.args.get('search',''))

    #进度条满时，跳转到主页
    if int(cur_num)==int(day_num):
        return redirect(url_for('main.home'))

    return render_template('abc.html',form=form,other_forms=other_form,word=word,times=times,means=means,cur_num=cur_num,day_num=day_num,
                           search=search,notes_list=notes_list)

#首页显示所有笔记，还是登录用户的个人笔记
@main.route('/show_all')
def show_all():
    resp=make_response(redirect(url_for('main.home')))
    resp.set_cookie('show_mine','',max_age=30*24*60*60)
    return resp

@main.route('/show_mine')
def show_mine():
    resp=make_response(redirect(url_for('main.home')))
    resp.set_cookie('show_mine','1',max_age=30*24*60*60)
    return resp

@main.route('/profile/<username>')
def profile(username):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='lshi6060660',
        db='shanbay',
        charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cur.execute('select email,gender,birthday,address,about_me,register_time,'
                'english_type,words_num_day from users where username="%s"'%username)
    info=cur.fetchone()

    cur.execute('select typename from type where id=%d'%int(info.get('english_type')))
    typename=cur.fetchone().get('typename')

    cur.close()
    conn.commit()
    conn.close()
    return render_template('profile.html',username=username,email=info.get('email'),gender=info.get('gender',''),birthday=info.get('birthday',''),
                           address=info.get('address',''),about_me=info.get('about_me',''),english_type=typename,num=info.get('words_num_day'),
                           register_time=info.get('register_time'))
# @main.route('/add_agree')
# def add_agree():
#     info=request.args.get('info')
#     aa=type(info)
#     return '<h1>%s</h1>'%aa

