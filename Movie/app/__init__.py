# -*- coding:utf-8 -*-
import os

__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:37'
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'zDJkOqA5xDugTzSaTEk5g/dGqIoZjuw+j9e/jBvTeizbko/CFQb5TZQHek2zUpvU'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/users')
app.debug = False
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


# 定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404