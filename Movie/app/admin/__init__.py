# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:37'
from flask import Blueprint

admin = Blueprint('admin', __name__)

import app.admin.views
