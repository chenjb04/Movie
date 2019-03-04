# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:37'
from datetime import datetime
from app import db


class User(db.Model):
    """会员"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 姓名
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    info = db.Column(db.Text)  # 简介
    face = db.Column(db.String(255), unique=True)  # 头像
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    user_logs = db.relationship('UserLog', backref='user')  # 会员日志外键关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关联
    movieCols = db.relationship('MovieCol', backref='user')  # 收藏外键关联

    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class UserLog(db.Model):
    """会员登录日志"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # ip地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return '<UserLog %r>' % self.id


class Tag(db.Model):
    """标签"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 关联电影

    def __repr__(self):
        return '<Tag %r>' % self.name


class Movie(db.Model):
    """电影"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 电影路由
    info = db.Column(db.Text)  # 电影简介
    logo = db.Column(db.String(255), unique=True)  # 电影图标
    star = db.Column(db.SmallInteger)  # 星级
    play_num = db.Column(db.BigInteger)  # 播放量
    comment_num = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放长度
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='movie')  # 评论外键关联
    movieCols = db.relationship('MovieCol', backref='movie')  # 收藏外键关联

    def __repr__(self):
        return '<Movie %r>' % self.title


class Preview(db.Model):
    """预告上映模型"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 名称
    logo = db.Column(db.String(255), unique=True)  # 电影图标
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title


class Comment(db.Model):
    """评论"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Comment %r>' % self.id


class MovieCol(db.Model):
    """电影收藏"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<MovieCol %r>' % self.id


class Auth(db.Model):
    """权限"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name


class Role(db.Model):
    """角色"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 管理员外键关联

    def __repr__(self):
        return '<Role %r>' % self.name


class Admin(db.Model):
    """管理员"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员 0是
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminLogs = db.relationship("AdminLog", backref='admin')  # 登录日志关联
    opLogs = db.relationship("OpLog", backref='admin')  # 操作日志关联

    def __repr__(self):
        return '<Admin %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class AdminLog(db.Model):
    """管理员登录日志"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # ip地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return '<AdminLog %r>' % self.id


class OpLog(db.Model):
    """操作日志"""
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # ip地址
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return '<OpLog %r>' % self.id


# if __name__ == '__main__':
#     # db.create_all()
#     admin = Admin(iname="chen", pwd=generate_password_hash("123456"),role_id=1
# )
#     db.session.add(admin)
#     db.session.commit()



