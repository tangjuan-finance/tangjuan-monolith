from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(("使用者名稱"), validators=[DataRequired()])
    password = PasswordField(("密碼"), validators=[DataRequired()])
    remember_me = BooleanField(("是否記住我的帳號"))
    submit = SubmitField(("登入"))


class RegistrationForm(FlaskForm):
    username = StringField(("使用者名稱"), validators=[DataRequired()])
    email = StringField(("電子信箱"), validators=[DataRequired(), Email()])
    password = PasswordField(("密碼"), validators=[DataRequired()])
    password2 = PasswordField(
        ("重複輸入密碼"), validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(("註冊"))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("請使用別的使用者名稱")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("請使用別的電子信箱")
