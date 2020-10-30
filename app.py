from flask import Flask, render_template, redirect, url_for, request, session, g, views, flash

import config
from exts import db
from decorators import login_required
from models import *
from forms import *

"""
这里是智能导学系统的app模块
"""

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/index')
@login_required
def index():
    return render_template('index.html')
    # return redirect(url_for('add_club'))


# 在请求之前进行的检测，修饰函数。用来确定g的数据的
@app.before_request
def before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user:
            g.user = user


# 登录视图函数
class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                session['user_id'] = user.id
                # if remember:
                # 如果设置sesion.premanent = True
                # 过期时间为30天
                # session.permanent = True
                return redirect(url_for('index'))
            else:
                # flash('邮箱或密码错误')
                return self.get(message='邮箱或密码错误')
        else:
            message = form.get_error()
            # print(message)
            return self.get(message=message)


# 绑定视图函数
app.add_url_rule('/', view_func=LoginView.as_view('/'))


# 注销视图函数
@app.route('/logout')
@login_required
def logout():
    # session.clear()
    del session['user_id']
    return redirect(url_for('/'))


# 注册用户函数
class AddUserView(views.MethodView):

    def get(self, message=None):
        return render_template('register.html', message=message)

    def post(self):
        form = RegisterForm(request.form)
        email = form.email.data
        username = form.username.data
        password = form.password.data
        schoolname = form.schoolname.data
        grade = form.grade.data
        userage = form.userage.data
        usergender = form.usergender.data
        # print(email)
        # print('数据获取')
        # print(form.validate())
        """
        context = {
            'oldusername': username,
            'email': email,
            'password': password,
            'grade': grade,
            'userage': userage,
            'usergender': usergender,
            'schoolname': schoolname
        }"""
        if form.validate():

            user = User(username=username,
                        parent_id=2,
                        email=email,
                        password=password,
                        role_permission=3,
                        grade=grade,
                        userage=userage,
                        usergender=usergender,
                        schoolname=schoolname)
            if not User.query.filter_by(email=email).first():
                db.session.add(user)
                db.session.commit()
                # print('注册正常')
                # flash('添加用户'+username+'成功')
                # message = '注册成功，请登录'
                return redirect(url_for('/'))
            else:
                flash("该邮箱已被注册！请更换邮箱!")
                message = "该邮箱已被注册！请更换邮箱!"
                return render_template('login.html', message=message)
        else:
            flash(form.get_error())
            message = form.get_error()
            return self.get(message=message)


# 绑定函数
app.add_url_rule('/register', view_func=AddUserView.as_view('register'))


@app.route('/club_list')
@login_required
def club_list():
    all_club = Club.query.filter().order_by(Club.join_time.desc())
    context = {'all_club': all_club}
    return render_template('club_list.html', **context)


@app.route('/add_club', methods=['GET', 'POST'])
@login_required
def add_club():
    if request.method == 'POST':
        print(request.form)
        form = ClubForm(request.form)
        print(form.name.data)
        print(form.name)
        name = form.name.data
        describe = form.describe.data
        teacher = form.teacher.data
        president = form.president.data
        print(name)
        one_club = Club(name=name, describe=describe, teacher=teacher, president=president)
        db.session.add(one_club)
        db.session.commit()
        return redirect(url_for('club_list'))
    if request.method == 'GET':
        return render_template('add_club.html')


@app.route('/edit_club/<club_id>', methods=['GET', 'POST'])
@login_required
def edit_club(club_id):
    if request.method == 'POST':
        form = ClubForm(request.form)
        name = form.name.data
        describe = form.describe.data
        teacher = form.teacher.data
        president = form.president.data
        one_club = Club.query.filter_by(id=club_id).first()
        one_club.name = name
        one_club.describe = describe
        one_club.teacher = teacher
        one_club.president = president
        db.session.commit()
        return redirect(url_for('club_list'))
    if request.method == 'GET':
        one_club = Club.query.filter_by(id=club_id).first()
        context = {'one_club': one_club}
        return render_template('edit_club.html', **context)


@app.route('/delete_club/<club_id>')
@login_required
def delete_club(club_id):
    one_club = Club.query.filter_by(id=club_id).first()
    db.session.delete(one_club)
    db.session.commit()
    return redirect(url_for('club_list'))


@app.route('/show_club/<club_id>')
@login_required
def show_club(club_id):
    one_club = Club.query.filter_by(id=club_id).first()
    context = {'one_club': one_club}
    return render_template('show_club.html', **context)


if __name__ == '__main__':
    app.run()
