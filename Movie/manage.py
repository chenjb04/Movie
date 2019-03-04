# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:36'
from flask_script import Manager
from app import app

manger = Manager(app)

if __name__ == '__main__':
    manger.run()