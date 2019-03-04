# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:38'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    """会员注册"""
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入昵称')],
        description='昵称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入昵称!'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码！')],
        description='密码',
        render_kw={'class': "form-control input-lg", 'placeholder': '请输入密码！'}
    )
    repeat_pwd = PasswordField(
        label='确认密码',
        validators=[DataRequired('请确认密码！'), EqualTo('pwd', message='两次密码不一致！')],
        description='确认密码',
        render_kw={'class': "form-control input-lg", 'placeholder': '请确认密码！'}
    )
    email = StringField(
        label='邮箱',
        validators=[DataRequired('请输入邮箱！'), Email("邮箱格式不正确")],
        description='邮箱',
        render_kw={'class': "form-control input-lg", 'placeholder': '请输入邮箱！'}
    )
    phone = StringField(
        label='手机号',
        validators=[DataRequired('请输入手机号！'), Regexp('^1[3458]\d{9}', message='手机号码格式不正确')],
        description='手机号',
        render_kw={'class': "form-control input-lg", 'placeholder': '请输入手机号！'}
    )
    submit = SubmitField(label='注册', render_kw={
        "class": 'btn btn-lg btn-success btn-block'
    })

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError('昵称已经存在')

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError('邮箱已经存在')

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError('手机已经存在')


class LoginForm(FlaskForm):
    """登录"""
    name = StringField(
        label='账号',
        validators=[DataRequired('请输入账号')],
        description='账号',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入用户名\手机号\邮箱!'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码！')],
        description='密码',
        render_kw={'class': "form-control input-lg", 'placeholder': '请输入密码！'}
    )
    submit = SubmitField(label='登录', render_kw={
        "class": 'btn btn-lg btn-success btn-block'
    })


class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入昵称')],
        description='昵称',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入昵称!'
        }
    )
    email = StringField(
        label='邮箱',
        validators=[DataRequired('请输入邮箱！'), Email("邮箱格式不正确")],
        description='邮箱',
        render_kw={'class': "form-control", 'placeholder': '请输入邮箱！'}
    )
    phone = StringField(
        label='手机号',
        validators=[DataRequired('请输入手机号！'), Regexp('^1[3458]\d{9}', message='手机号码格式不正确')],
        description='手机号',
        render_kw={'class': "form-control ", 'placeholder': '请输入手机号！'}
    )
    face = FileField(
        label='头像',
        validators=[DataRequired('请上传头像')],
        description='头像'
    )
    info = TextAreaField(
        label='简介',
        validators=[DataRequired('请输入简介')],
        description='简介',
        render_kw={
            'class': 'form-control',
            'rows': 10
        }
    )
    submit = SubmitField(label='保存修改', render_kw={
        "class": 'btn btn-success'
    })


class PwdForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField(
        label='旧密码',
        validators=[DataRequired('请输入旧密码！')],
        description='旧密码',
        render_kw={'class': "form-control", 'placeholder': '请输入旧密码！'}
    )
    new_password = PasswordField(
        label='新密码',
        validators=[DataRequired('请输入新密码！')],
        description='新密码',
        render_kw={'class': "form-control", 'placeholder': '请输入新密码！'}
    )
    submit = SubmitField(label='修改密码', render_kw={
        "class": 'btn btn-primary'
    })

    def validate_old_password(self, filed):
        from flask import session
        pwd = filed.data
        name = session['user']
        user = User.query.filter_by(name=name).first()
        if not user.check_pwd(pwd):
            raise ValidationError('旧密码错误')


class CommentForm(FlaskForm):
    """评论表单"""
    content = TextAreaField(
        label='内容',
        description='内容',
        validators=[DataRequired('请输入评论的内容！')],
        render_kw={
            'id': 'input_content',
        }
    )
    submit = SubmitField(label='提交评论', render_kw={
        "class": 'btn btn-success',
        'id': 'btn-sub',
    })