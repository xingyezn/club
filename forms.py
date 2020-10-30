from wtforms import Form, StringField, IntegerField, ValidationError, FloatField
from wtforms.validators import Email, InputRequired, Length, EqualTo
# 用来邮箱验证的
import cache
from models import User
from flask import g


class BaseForms(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


# 登录界面的form表单检测
class LoginForm(BaseForms):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱！')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])


# 注册用户的表单检测
class RegisterForm(BaseForms):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱！')])
    username = StringField(validators=[InputRequired(message='请输入用户名')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    repassword = StringField(validators=[EqualTo("password", message='密码必须保持一致')])
    schoolname = StringField(validators=[InputRequired(message='请输入学校姓名')])
    grade = IntegerField(validators=[InputRequired(message='请选择用户年级')])
    userage = IntegerField(validators=[InputRequired(message='请选择用户年龄')])
    usergender = IntegerField(validators=[InputRequired(message='请选择用户性别')])

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('该邮箱已被注册请另外选择邮箱！')


class ClubForm(BaseForms):
    name = StringField(validators=[InputRequired(message='请输入数据')])
    describe = StringField(validators=[InputRequired(message='请输入数据')])
    teacher = StringField(validators=[InputRequired(message='请输入数据')])
    president = StringField(validators=[InputRequired(message='请输入数据')])


"""
# 重置密码的表单检测
class ResetpwdForm(BaseForms):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='确认密码必须和新密码保持一致')])

# 重置邮箱的表单检测
class ResetEmailForm(BaseForms):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正常长度的验证码！')])

    def validate_captcha(self,field):
        #表单提交的验证码
        captcha = field.data
        # 表单提交的email
        email = self.email.data
        # 缓存email
        
        captcha_cache = cache.get(email)
        print(captcha)
        print(captcha_cache)
        if not captcha_cache and captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')


    def validate_email(self,field):
        email = field.data
        user = g.user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱！')

"""
