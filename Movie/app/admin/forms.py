# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:38'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(label='账号', validators=[DataRequired('请输入账号!')], description='账号',
                          render_kw={"class": "form-control", "placeholder": '请输入账号！', "required": 'required'})

    pwd = PasswordField(label='密码', validators=[DataRequired('请输入密码!')], description='密码',
                        render_kw={"class": "form-control", "placeholder": '请输入密码！', "required": 'required'})

    submit = SubmitField(label='登录', render_kw={
        "class": 'btn btn-primary btn-block btn-flat'
    })

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


class TagForm(FlaskForm):
    """标签管理"""
    name = StringField(
        label='名称',
        validators=[DataRequired('请输入标签！')],
        description='标签',
        render_kw={'class': "form-control", 'id': 'input_name', 'placeholder': '请输入标签的名称！'}
    )
    submit = SubmitField(label='编辑', render_kw={
        "class": 'btn btn-primary'
    })


class MovieForm(FlaskForm):
    """电影表单"""
    title = StringField(
        label='片名',
        validators=[DataRequired('请输入片名！')],
        description='片名',
        render_kw={'class': "form-control", 'placeholder': '请输入片名！'}
    )
    url = FileField(
        label='文件',
        validators=[DataRequired('请上传文件!')],
        description='文件'
    )
    info = TextAreaField(
        label='简介',
        validators=[DataRequired('请输入简介信息！')],
        description='简介',
        render_kw={'class': "form-control", 'placeholder': '请输入简介信息！', "rows": 10}
    )
    logo = FileField(
        label='封面',
        validators=[DataRequired('请上传封面!')],
        description='封面'
    )
    star = SelectField(
        label='星级',
        validators=[DataRequired('请选择星级')],
        description='星级',
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        render_kw={'class': "form-control"}

    )
    tag_id = SelectField(
        label='标签',
        validators=[DataRequired('请选择标签')],
        description='所属标签',
        coerce=int,
        choices=[(tag.id, tag.name) for tag in Tag.query.all()],
        render_kw={'class': "form-control"}
    )
    area = StringField(
        label='地区',
        validators=[DataRequired('请输入地区！')],
        description='地区',
        render_kw={'class': "form-control", 'placeholder': '请输入地区！'}
    )
    length = StringField(
        label='片长',
        validators=[DataRequired('请输入片长！')],
        description='片长',
        render_kw={'class': "form-control", 'placeholder': '请输入片长！'}
    )
    release_time =StringField(
        label="上映时间",
        validators=[
            DataRequired("上映时间不能为空！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(label='编辑', render_kw={
        "class": 'btn btn-primary'
    })


class PreviewForm(FlaskForm):
    """电影预告"""
    title = StringField(
        label='预告片名',
        validators=[DataRequired('请输入预告片名！')],
        description='片名',
        render_kw={'class': "form-control", 'placeholder': '请输入预告片名！'}
    )
    logo = FileField(
        label='封面',
        validators=[DataRequired('请上传封面!')],
        description='封面'
    )
    submit = SubmitField(label='编辑', render_kw={
        "class": 'btn btn-primary'
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
    submit = SubmitField(label='修改', render_kw={
        "class": 'btn btn-primary'
    })

    def validate_old_password(self, filed):
        from flask import session
        pwd = filed.data
        name = session['admin']
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError('旧密码错误')


class AuthForm(FlaskForm):
    """权限管理表单"""
    name = StringField(
        label='权限名',
        validators=[DataRequired('请输入权限名！')],
        description='权限名',
        render_kw={'class': "form-control", 'placeholder': '请输入权限名！'}
    )
    url = StringField(
        label='权限路径名',
        validators=[DataRequired('请输入路径名！')],
        description='权限路径名',
        render_kw={'class': "form-control", 'placeholder': '请输入权限路径名！'}
    )

    submit = SubmitField(label='编辑', render_kw={
        "class": 'btn btn-primary'
    })


class RoleForm(FlaskForm):
    """角色表单"""
    name = StringField(
        label='角色名',
        validators=[DataRequired('请输入角色名！')],
        description='角色名',
        render_kw={'class': "form-control", 'placeholder': '请输入角色名！'}
    )
    auth_list = SelectMultipleField(
        label='权限列表',
        validators=[DataRequired('请选择权限列表')],
        description='权限列表',
        coerce=int,
        choices=[(auth.id, auth.name) for auth in Auth.query.all()],
        render_kw={'class': "form-control"}
    )
    submit = SubmitField(label='编辑', render_kw={
        "class": 'btn btn-primary'
    })


class AdminForm(FlaskForm):
    """管理员表单"""
    name = StringField(
        label='管理员名称',
        validators=[DataRequired('请输入管理员名称！')],
        description='管理员名称',
        render_kw={'class': "form-control", 'placeholder': '请输入管理员名称！'}
    )
    pwd = PasswordField(
        label='管理员密码',
        validators=[DataRequired('请输入管理员密码！')],
        description='管理员密码',
        render_kw={'class': "form-control", 'placeholder': '请输入管理员密码！'}
    )
    repeat_pwd = PasswordField(
        label='管理员重复密码',
        validators=[DataRequired('请输入管理员重复密码！'), EqualTo('pwd', message='两次密码不一致！')],
        description='管理员重复密码',
        render_kw={'class': "form-control", 'placeholder': '请输入管理员重复密码！'}
    )
    role_id = SelectField(
        label='所属角色',
        coerce=int,
        choices=[(rol.id, rol.name) for rol in Role.query.all()],
        description='所属角色',
        render_kw={'class': "form-control"}
    )
    submit = SubmitField(label='编辑', render_kw={
        "class": 'btn btn-primary'
    })
