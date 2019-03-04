# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:37'
from flask import Blueprint

home = Blueprint('home', __name__)

import app.home.views
