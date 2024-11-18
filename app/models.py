from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class TimestampMixin:
    created: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    updated: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(UserMixin, TimestampMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class ScenarioExpense(db.Model):
    left_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("scenario.id"), primary_key=True)
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("expense.id"), primary_key=True
    )
    upper_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="expense")
    expense: so.Mapped["Expense"] = so.relationship(back_populates="scenario")

class Scenario(TimestampMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    expense: so.Mapped[list["ScenarioExpense"]] = so.relationship(back_populates="scenario")

    def __repr__(self):
        return '<Scenario {}>'.format(self.name)

class Expense(TimestampMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    amount: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    scenario: so.Mapped[list["ScenarioExpense"]] = so.relationship(back_populates="expense")

    def __repr__(self):
        return '<Expense {}>'.format(self.name)