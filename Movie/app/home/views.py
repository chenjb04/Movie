# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:38'
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from .forms import RegisterForm, LoginForm, UserDetailForm, PwdForm, CommentForm
import uuid
from werkzeug.security import generate_password_hash
from app.models import User, UserLog, Preview, Tag, Movie, Comment, MovieCol
from app import db
from app import app
from functools import wraps
import os
import json
from werkzeug.utils import secure_filename
from ..admin.views import change_filename


def user_login_req(f):
    """登录权限限制"""
    @wraps(f)
    def deco(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)
    return deco


@home.route('/<int:page>/', methods=['GET'])
def index(page):
    tags = Tag.query.all()
    page_data = Movie.query

    tag_id = request.args.get('tag_id', 0)
    if int(tag_id) != 0:
        page_data = page_data.filter_by(tag_id=tag_id)

    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))

    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(Movie.add_time.desc())
        if int(time)  == 2:
            page_data = page_data.order_by(Movie.add_time.asc())

    play_num = request.args.get('play_num', 0)
    if int(play_num) != 0 :
        if int(play_num) == 1:
            page_data = page_data.order_by(Movie.play_num.desc())
        if int(play_num) == 2:
            page_data = page_data.order_by(Movie.play_num.asc())

    comment_num = request.args.get('comment_num', 0)
    if int(comment_num) != 0:
        if int(comment_num) == 1:
            page_data = page_data.order_by(Movie.comment_num.desc())
        if int(comment_num) == 2:
            page_data = page_data.order_by(Movie.comment_num.asc())

    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=8)
    p = dict(tag_id=tag_id, star=star, time=time, play_num=play_num, comment_num=comment_num)
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


@home.route('/login', methods=['POST', 'GET'])
def login():
    """登录"""
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if user is None:
            user = User.query.filter_by(email=data['name']).first()
            if user is None:
                user = User.query.filter_by(phone=data['name']).first()
                if user is None:
                    flash("用户不存在", 'error')
        if user:
            if not user.check_pwd(data['pwd']):
                flash('密码错误', 'error')
                return redirect(url_for('home.login'))
            session['user'] = user.name
            session['user_id'] = user.id
            user_log = UserLog(
                user_id=user.id,
                ip=request.remote_addr
            )
            db.session.add(user_log)
            db.session.commit()
            return redirect(url_for('home.user'))
    return render_template('home/login.html', form=form)


@home.route('/logout')
def logout():
    """退出"""
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


@home.route('/register', methods=['POST', 'GET'])
def register():
    """会员注册"""
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex,
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功', 'success')
    return render_template('home/register.html', form=form)


@home.route('/user', methods=['POST', 'GET'])
@user_login_req
def user():
    """会员中心资料修改"""
    form = UserDetailForm()
    user = User.query.get(int(session['user_id']))
    form.face.validators = []
    form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if form.face.data.filename != "":
            file_face = secure_filename(form.face.data.filename)
            if not os.path.exists(app.config["FC_DIR"]):
                os.makedirs(app.config["FC_DIR"])
                os.chmod(app.config["FC_DIR"])
            user.face = change_filename(file_face)
            form.face.data.save(app.config["FC_DIR"] + user.face)

        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在!", "error")
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在!", "error")
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("手机已经存在!", "error")

            return redirect(url_for("home.user"))
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


@home.route('/pwd', methods=['POST', 'GET'])
@user_login_req
def pwd():
    """修改密码"""
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.get_or_404(session['user_id'])
        user.pwd = generate_password_hash(data['new_password'])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功,请重新登录', 'success')
        redirect(url_for('home.logout', next='admin.login'))
    return render_template('home/pwd.html', form=form)


@home.route('/comments/<int:page>')
@user_login_req
def comments(page):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Movie.id == Comment.movie_id,
                                                                User.id == session['user_id']).order_by(
            Comment.add_time.desc()).paginate(page=page, per_page=6)
    return render_template('home/comments.html', page_data=page_data)


@home.route('/loginlog/<int:page>')
@user_login_req
def login_log(page):
    """会员登录日志"""
    if page is None:
        page = 1
    page_data = UserLog.query.join(User).filter(User.id == UserLog.user_id).order_by(UserLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('home/loginlog.html', page_data=page_data)


@home.route('/moviecol/add/')
@user_login_req
def movie_col_add():
    """添加电影收藏"""
    movie_id = int(request.args.get('mid'))
    user_id = int(request.args.get('uid'))
    movie_col_count = MovieCol.query.filter_by(movie_id=movie_id, user_id=user_id).count()
    data = None
    if movie_col_count == 1:
        data = {"ok": 1}
    if movie_col_count == 0:
        movie_col = MovieCol(movie_id=movie_id, user_id=user_id)
        db.session.add(movie_col)
        db.session.commit()
        data = {"ok": 0}
    return json.dumps(data)


@home.route('/moviecol/<int:page>')
@user_login_req
def movie_col(page):
    """电影收藏"""
    if page is None:
        page = 1
    page_data = MovieCol.query.order_by(MovieCol.add_time.desc()).paginate(page=page, per_page=6)
    return render_template('home/moviecol.html', page_data=page_data)


@home.route('/animation')
def animation():
    """点影上映预告"""
    data = Preview.query.all()
    return render_template('home/animation.html', data=data)


@home.route('/search/<int:page>/')
def search(page):
    """搜索"""
    key = request.args.get('key', '')
    if page is None:
        page = 1
    movie_count = Movie.query.filter(Movie.title.ilike('%'+key+'%')).count()
    page_data = Movie.query.filter(Movie.title.ilike('%'+key+'%')).order_by(Movie.add_time.desc()).paginate(page=page, per_page=5)
    page_data.key = key
    return render_template('home/search.html', key=key, page_data=page_data, movie_count=movie_count)


@home.route('/play/<int:id>/<int:page>', methods=['POST', 'GET'])
def play(id, page):
    """电影播放"""
    movie = Movie.query.join(Tag).filter(Movie.tag_id == Tag.id, Movie.id == id).first_or_404()
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Movie.id == movie.id, User.id == Comment.user_id).order_by(Comment.add_time.desc()).paginate(page=page, per_page=6)
    comment_count = Comment.query.join(Movie).filter(Movie.id == movie.id).count()
    form = CommentForm()
    if 'user'in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            user_id=session['user_id'],
            movie_id=movie.id
        )
        db.session.add(comment)
        db.session.commit()
        movie.comment_num += 1
        db.session.add(movie)
        db.session.commit()
        flash('评论成功', 'success')
        return redirect(url_for('home.play', id=movie.id, page=1))
    movie.play_num += 1
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data, comment_count=comment_count)

