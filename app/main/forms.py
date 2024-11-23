from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField("使用者名稱", validators=[DataRequired()])
    about_me = TextAreaField("關於我", validators=[Length(min=0, max=140)])
    submit = SubmitField("送出")

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(
                sa.select(User).where(User.username == username.data)
            )
            if user is not None:
                raise ValidationError("請使用別的使用者名稱")


class EmptyForm(FlaskForm):
    submit = SubmitField("送出")


class IndexAnonyServiceForm(FlaskForm):
    start_year = IntegerField(
        "起始年齡",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=150, message="輸入請介於 0 到 150 歲之間"),
        ],
        description="通常會是您現在的年齡",
        default=26,
    )
    investment_amount = IntegerField(
        "起始總投資金額",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10e12, message="輸入請介於 0 到百億之間"),
        ],
        description="通常會是您現在的總投資額。單位：元",
        default=1000000,
    )
    expense_amount = IntegerField(
        "起始生活費",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10e7, message="輸入請介於 0 到百萬之間"),
        ],
        description="每月平均生活費。單位：元",
        default=10000,
    )
    salary_amount = IntegerField(
        "起始薪資",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10e12, message="輸入請介於 0 到百億之間"),
        ],
        description="通常會是您現在的月薪。單位：元",
        default=36000,
    )
    house_start_year = IntegerField(
        "購屋時年齡",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=150, message="輸入請介於 0 到 150 歲之間"),
        ],
        description="單位：歲",
        default=36,
    )
    house_amount = FloatField(
        "房屋總價",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10e12, message="輸入請介於 0 到百億之間"),
        ],
        description="單位：元",
        default=10000000,
    )
    down_payment = FloatField(
        "頭期款金額",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10e12, message="輸入請介於 0 到百億之間"),
        ],
        description="單位：元",
        default=2000000,
    )
    interest = FloatField(
        "年利率",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100, message="輸入請介於 0 到 100 之間"),
        ],
        description="單位：%",
        default=1.05,
    )
    loan_term = IntegerField(
        "貸款年限",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=150, message="輸入請介於 0 到 40 年之間"),
        ],
        description="單位：年",
        default=30,
    )
    child_born_at_age = IntegerField(
        "預計生小孩時年齡",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=150, message="輸入請介於 0 到 150 歲之間"),
        ],
        description="單位：歲",
        default=34,
    )
    investment_ratio = FloatField(
        "餘額轉投資比率",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100, message="輸入請介於 0 到 100 之間"),
        ],
        description="每個月剩餘收入作為投資的比例。單位：%",
        default=70,
    )
    retire_age = IntegerField(
        "退休年齡",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=150, message="輸入請介於 0 到 150 歲之間"),
        ],
        description="單位：歲",
        default=65,
    )
    submit = SubmitField("送出")
