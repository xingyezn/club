from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash


class CMSPermission(object):
    # 开发者管理员
    DEVELOPER = 1
    # 教师
    TEACHER = 2
    # 学校管理员
    STUDENT = 3


class Role(db.Model):
    # 用户角色表
    __tablename__ = 'role'
    # 角色名称
    name = db.Column(db.String(50), nullable=False)
    # 角色描述
    desc = db.Column(db.String(200), nullable=True)
    # 用户权限（主键）
    permission = db.Column(db.Integer, nullable=False, primary_key=True)


user_club_table = db.Table('user_club_table', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('club_id', db.Integer, db.ForeignKey('club.id')))


class User(db.Model):
    # 用户信息表
    __tablename__ = 'user'
    # 用户id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #  一下是必须填写的信息
    # 用户姓名
    username = db.Column(db.String(50), nullable=False)
    # 用户学校
    schoolname = db.Column(db.String(100), nullable=True)
    # 年龄
    userage = db.Column(db.Integer, nullable=True)
    # 性别 1代表男，2代表女
    usergender = db.Column(db.Integer, nullable=True)
    # 年级，1-12表示K12
    grade = db.Column(db.Integer, nullable=True)
    # 用户密码
    password = db.Column(db.String(100), nullable=False)
    # 用户邮箱
    email = db.Column(db.String(50), nullable=False, unique=True)
    # 这些信息都是自动生成的
    # 添加时间
    join_time = db.Column(db.DateTime, default=datetime.now)
    # 角色权限
    role_permission = db.Column(db.Integer, db.ForeignKey('role.permission'))
    # 用户角色
    user_role = db.relationship('Role', backref='role_users')
    parent_id = db.Column(db.Integer, default=None, nullable=True)
    # 这些信息可以后续完善，现在只需要简单的一些信息即可
    # 用户省份
    province = db.Column(db.String(100), default=None, nullable=True)
    # 用户城市
    city = db.Column(db.String(100), default=None, nullable=True)
    # 用户地区
    county = db.Column(db.String(100), default=None, nullable=True)
    user_club = db.relationship('Club', secondary=user_club_table, back_populates='club_user')


class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(2000), nullable=True)
    teacher = db.Column(db.String(50), nullable=True)
    president = db.Column(db.String(50), nullable=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    club_user = db.relationship('User', secondary=user_club_table, back_populates='user_club')


class JoinClub(db.Model):
    __tablename__ = 'join_club'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    join_user = db.relationship('User', backref='user_join')
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    join_target_club = db.relationship('Club', backref='club_join')
    agree = db.Column(db.Integer, default=0)
    join_time = db.Column(db.DateTime, default=datetime.now)
