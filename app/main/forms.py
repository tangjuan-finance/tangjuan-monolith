from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
import sqlalchemy as sa
from app import db
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('使用者名稱', validators=[DataRequired()])
    about_me = TextAreaField('關於我',
                             validators=[Length(min=0, max=140)])
    submit = SubmitField('送出')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('請使用別的使用者名稱')


class EmptyForm(FlaskForm):
    submit = SubmitField('送出')