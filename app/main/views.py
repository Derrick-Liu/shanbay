#coding:utf-8
from . import main
from flask import render_template,redirect,url_for

@main.route('/')
def home():
    return render_template('home_page.html')