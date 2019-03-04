# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/9/20 18:38'
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from .forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, MovieCol, OpLog, AdminLog, UserLog, Auth, Role
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash


def admin_login_req(f):
    """登录权限限制"""
    @wraps(f)
    def deco(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return deco


def change_filename(filename):
    """修改上传文件的名字"""
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


def admin_auth(f):
    """权限访问控制装饰器"""
    @wraps(f)
    def deco(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session["admin_id"]
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(",")))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
        return f(*args, **kwargs)
    return deco


@admin.context_processor
def tpl_extra():
    """上下文管理器"""
    data = dict(online_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return data


@admin.route('/')
@admin_login_req
@admin_auth
def index():
    return render_template('admin/index.html')


@admin.route('/login', methods=["GET", "POST"])
def login():
    """后台登录"""
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash('密码错误')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        session['admin_id'] = admin.id
        admin_login = AdminLog(admin_id=session['admin_id'],ip=request.remote_addr)
        db.session.add(admin_login)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('admin.index'))

    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@admin_login_req
def logout():
    """后台退出"""
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


@admin.route('/pwd', methods=['POST', 'GET'])
@admin_login_req
def pwd():
    """修改密码"""
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        admin.pwd = generate_password_hash(data['new_password'])
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功,请重新登录', 'success')
        redirect(url_for('admin.logout', next='admin.login'))
    return render_template('admin/pwd.html', form=form)


@admin.route('/tag/add', methods=['POST', 'GET'])
@admin_login_req
@admin_auth
def tag_add():
    """添加标签"""
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('名称已经存在', 'error')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功', 'success')
        oplog = OpLog(
            admin_id=session['admin_id'], ip=request.remote_addr, reason='添加标签%s成功' % data['name']
        )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


@admin.route('/tag/list/<int:page>/')
@admin_login_req
@admin_auth
def tag_list(page=None):
    """标签列表页"""
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/tag_list.html', page_data=page_data)


@admin.route('/tag/del/<int:id>/')
@admin_login_req
@admin_auth
def del_tag(id):
    """删除标签"""
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.tag_list', page=1))


@admin.route('/tag/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def edit_tag(id):
    """编辑标签"""
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash('名称已经存在', 'error')
            return redirect(url_for('admin.edit_tag', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功', 'success')
        redirect(url_for('admin.edit_tag', id=id))
    return render_template('admin/edit_tag.html', form=form, tag=tag)


@admin.route('/movie/add', methods=["GET", "POST"])
@admin_login_req
# @admin_auth
def movie_add():
    """添加电影"""
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 777)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR']+url)
        form.logo.data.save(app.config['UP_DIR']+logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            play_num=0,
            comment_num=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'success')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


@admin.route('/movie/list/<int:page>')
@admin_login_req
@admin_auth
def movie_list(page):
    """电影列表"""
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(Tag.id == Movie.tag_id).\
        order_by(Movie.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/movie_list.html', page_data=page_data)


@admin.route('/movie/del/<int:id>/')
@admin_login_req
def del_movie(id):
    """删除电影"""
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.movie_list', page=1))


@admin.route('/movie/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def edit_movie(id):
    """编辑电影"""
    form = MovieForm()
    movie = Movie.query.get_or_404(int(id))
    if request.method == "GET":
        form.url.data = []
        form.logo.data = []
        form.info.data = movie.info
        form.star.data = movie.star
        form.tag_id.data = movie.tag_id
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_count == 1 and movie.title != data['title']:
            flash('片名存在修改失败', 'error')
            return redirect(url_for('admin.edit_movie', id=movie.id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 777)
        if form.url.data.filename != '':
            file_url = secure_filename(form.url.data.filename)
            url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + url)
        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + logo)
        movie.url = url
        movie.logo = logo
        movie.title = data['title']
        movie.info = data['info']
        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.area = data['area']
        movie.length = data['length']
        movie.release_time = data['release_time']
        db.session.add(movie)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('admin.edit_movie', id=movie.id))
    return render_template('admin/edit_movie.html', form=form, movie=movie)


@admin.route('/preview/add', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def preview_add():
    """预告添加"""
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 777)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = Preview()
        preview.title = data['title']
        preview.logo = logo
        db.session.add(preview)
        db.session.commit()
        flash('添加成功', 'success')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


@admin.route('/preview/list/<int:page>')
@admin_login_req
@admin_auth
def preview_list(page):
    """预告列表"""
    if page is None:
        page = 1
    page_data = Preview.query.order_by(Preview.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/preview_list.html', page_data=page_data)


@admin.route('/preview/del/<int:id>')
@admin_login_req
@admin_auth
def preview_del(id):
    """预告删除"""
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.preview_list', page=1))


@admin.route('/preview/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_edit(id):
    """预告编辑"""
    form = PreviewForm()
    preview = Preview.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data['title']).count()
        if preview.title != data['title'] and preview_count == 1:
            flash('名称已经存在', 'error')
            return redirect(url_for('admin.preview_edit', id=id))
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 777)
        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + logo)
        preview.title = data['title']
        preview.logo = logo
        db.session.add(preview)
        db.session.commit()
        flash('修改预告成功', 'success')
        redirect(url_for('admin.preview_edit', id=id))
    return render_template('admin/edit_preview.html', form=form, preview=preview)


@admin.route('/user/list/<int:page>')
@admin_login_req
@admin_auth
def user_list(page):
    """会员列表"""
    if page is None:
        page = 1
    page_data = User.query.order_by(User.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/user_list.html', page_data=page_data)


@admin.route('/user/view/<int:id>')
@admin_login_req
@admin_auth
def user_view(id):
    """查看会员"""
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html', user=user)


@admin.route('/user/del/<int:id>/')
@admin_login_req
@admin_auth
def del_user(id):
    """删除会员"""
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.user_list', page=1))


@admin.route('/comment/list/<int:page>')
@admin_login_req
@admin_auth
def comment_list(page):
    """评论列表"""
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Movie.id == Comment.movie_id, User.id == Comment.user_id).order_by(Comment.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/comment_list.html', page_data=page_data)


@admin.route('/comment/del/<int:id>/')
@admin_login_req
@admin_auth
def del_comment(id):
    """删除评论"""
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.comment_list', page=1))


@admin.route('/moviecol/del/<int:id>')
@admin_login_req
@admin_auth
def moviecol_del(id):
    """电影收藏删除"""
    movie_col = MovieCol.query.filter_by(id=id).first_or_404()
    db.session.delete(movie_col)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.moviecol_list', page=1))


@admin.route('/moviecol/list/<int:page>')
@admin_login_req
@admin_auth
def moviecol_list(page):
    """电影收藏列表"""
    if page is None:
        page = 1
    page_data = MovieCol.query.join(Movie).join(User).filter(Movie.id == MovieCol.movie_id, User.id == MovieCol.user_id).order_by(MovieCol.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/moviecol_list.html', page_data=page_data)


@admin.route('/oplog/list/<int:page>')
@admin_login_req
@admin_auth
def oplog_list(page):
    """操作日志列表"""
    if page is None:
        page = 1
    page_data = OpLog.query.join(Admin).filter(Admin.id == OpLog.admin_id).order_by(OpLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/oplog_list.html', page_data=page_data)


@admin.route('/adminloginlog/list/<int:page>')
@admin_login_req
@admin_auth
def adminloginlog_list(page):
    """管理员登录日志列表"""
    if page is None:
        page = 1
    page_data = AdminLog.query.join(Admin).filter(Admin.id == AdminLog.admin_id).order_by(AdminLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/adminloginlog_list.html', page_data=page_data)


@admin.route('/userloginlog/list/<int:page>')
@admin_login_req
@admin_auth
def userloginlog_list(page):
    """会员登录日志列表"""
    if page is None:
        page = 1
    page_data = UserLog.query.join(User).filter(User.id == UserLog.user_id).order_by(
        UserLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/userloginlog_list.html', page_data=page_data)


@admin.route('/auth/add', methods=['POST', 'GET'])
@admin_login_req
@admin_auth
def auth_add():
    """添加权限"""
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(name=data['name'], url=data['url'])
        db.session.add(auth)
        db.session.commit()
        flash('添加权限成功', 'success')
    return render_template('admin/auth_add.html', form=form)


@admin.route('/auth/list/<int:page>')
@admin_login_req
@admin_auth
def auth_list(page):
    """权限列表"""
    if page is None:
        page = 1
    page_data = Auth.query.order_by(Auth.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/auth_list.html', page_data=page_data)


@admin.route('/auth/del/<int:id>/')
@admin_login_req
@admin_auth
def del_auth(id):
    """删除权限"""
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.auth_list', page=1))


@admin.route('/auth/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def edit_auth(id):
    """编辑权限"""
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data['name']).count()
        if auth.name != data['name'] and auth_count == 1:
            flash('名称已经存在', 'error')
            return redirect(url_for('admin.edit_auth', id=id))
        auth.name = data['name']
        auth.url = data['url']
        db.session.add(auth)
        db.session.commit()
        flash('修改权限成功', 'success')
        redirect(url_for('admin.edit_auth', id=id))
    return render_template('admin/edit_auth.html', form=form, auth=auth)


@admin.route('/role/add', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_add():
    """添加角色"""
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(name=data['name'], auths=",".join(map(lambda i: str(i), data['auth_list'])))
        db.session.add(role)
        db.session.commit()
        flash('添加成功', 'success')
    return render_template('admin/role_add.html', form=form)


@admin.route('/role/list/<int:page>')
@admin_login_req
@admin_auth
def role_list(page):
    """角色列表"""
    if page is None:
        page = 1
    page_data = Role.query.order_by(Role.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/role_list.html', page_data=page_data)


@admin.route('/role/del/<int:id>/')
@admin_login_req
@admin_auth
def del_role(id):
    """删除角色"""
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.role_list', page=1))


@admin.route('/role/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def edit_role(id):
    """编辑角色"""
    form = RoleForm()
    role = Role.query.get_or_404(id)
    form.auth_list.data = list(map(lambda i: int
    (i), role.auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role_count =Role.query.filter_by(name=data['name']).count()
        if role.name != data['name'] and role_count == 1:
            flash('名称已经存在', 'error')
            return redirect(url_for('admin.edit_role', id=id))

        role.name = data['name']
        role.auths = ",".join(map(lambda i: str(i), data['auth_list']))
        db.session.add(role)
        db.session.commit()
        flash('修改角色成功', 'success')
        redirect(url_for('admin.edit_role', id=id))
    return render_template('admin/edit_role.html', form=form, role=role)


@admin.route('/admin/add', methods=['POST', 'GET'])
@admin_login_req
@admin_auth
def admin_add():
    """添加管理员"""
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin(name=data['name'], pwd=generate_password_hash(data['repeat_pwd']), role_id=data['role_id'])
        db.session.add(admin)
        db.session.commit()
        flash('添加成功', 'success')
    return render_template('admin/admin_add.html', form=form)


@admin.route('/admin/list/<int:page>')
@admin_login_req
@admin_auth
def admin_list(page):
    """管理员列表"""
    if page is None:
        page = 1
    page_data = Admin.query.join(Role).filter(Admin.role_id == Role.id).order_by(Admin.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/admin_list.html', page_data=page_data)
