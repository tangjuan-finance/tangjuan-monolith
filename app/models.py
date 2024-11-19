from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

#Validation Tables
class Age(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    year: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

    def __repr__(self):
        return '<Age {} years>'.format(self.year)

#Mixin
class TimestampMixin:
    created: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    updated: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class BaseYearIntervalMixin:
    start_year: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Age.id))
    end_year: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Age.id))

class BaseDescriptionMixin:
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)

#Entity
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
    
    #One-to-Many Ownership
    scenarios: so.WriteOnlyMapped['Scenario'] = so.relationship(
        back_populates='owner')
    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(
        back_populates='owner')
    salaries: so.WriteOnlyMapped['Salary'] = so.relationship(
        back_populates='owner')
    investments: so.WriteOnlyMapped['Investment'] = so.relationship(
        back_populates='owner')
    houses: so.WriteOnlyMapped['House'] = so.relationship(
        back_populates='owner')    
    children: so.WriteOnlyMapped['Child'] = so.relationship(
        back_populates='owner')  
    
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

class Scenario(TimestampMixin, BaseDescriptionMixin,  db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    #Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='scenarios')

    #Many-to-Many Relationship
    expense: so.Mapped[list["ScenarioExpense"]] = so.relationship(back_populates="scenario")
    salary: so.Mapped[list["ScenarioSalary"]] = so.relationship(back_populates="scenario")
    investment: so.Mapped[list["ScenarioInvestment"]] = so.relationship(back_populates="scenario")
    house: so.Mapped[list["ScenarioHouse"]] = so.relationship(back_populates="scenario")
    child: so.Mapped[list["ScenarioChild"]] = so.relationship(back_populates="scenario")

    def __repr__(self):
        return '<Scenario {}>'.format(self.name)

class ScenarioExpense(BaseYearIntervalMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("scenario.id"), primary_key=True)
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("expense.id"), primary_key=True
    )
    upper_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="expense")
    expense: so.Mapped["Expense"] = so.relationship(back_populates="scenario")

class Expense(TimestampMixin, BaseYearIntervalMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)

    #Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='expenses')

    #Relationship to Scenario
    scenario: so.Mapped[list["ScenarioExpense"]] = so.relationship(back_populates="expense")

    def __repr__(self):
        return '<Expense {}>'.format(self.name)

class ScenarioSalary(BaseYearIntervalMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("scenario.id"), primary_key=True)
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("salary.id"), primary_key=True
    )
    upper_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="salary")
    salary: so.Mapped["Salary"] = so.relationship(back_populates="scenario")

class Salary(TimestampMixin, BaseYearIntervalMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)

    #Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='salaries')

    #Relationship to Scenario
    scenario: so.Mapped[list["ScenarioSalary"]] = so.relationship(back_populates="salary")

    def __repr__(self):
        return '<Salary {}>'.format(self.name)
    
class ScenarioInvestment(BaseYearIntervalMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("scenario.id"), primary_key=True)
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("investment.id"), primary_key=True
    )
    upper_return_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_return_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    percentage_from_saving: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="investment")
    investment: so.Mapped["Investment"] = so.relationship(back_populates="scenario")

class Investment(TimestampMixin, BaseYearIntervalMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)

    #Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='investments')

    #Relationship to Scenario
    scenario: so.Mapped[list["ScenarioInvestment"]] = so.relationship(back_populates="investment")

    def __repr__(self):
        return '<Investment {}>'.format(self.name)

class ScenarioHouse(db.Model):
    left_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("scenario.id"), primary_key=True)
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("house.id"), primary_key=True
    )
    buy_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Age.id))
    sell_at_age: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Age.id))
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="house")
    house: so.Mapped["House"] = so.relationship(back_populates="scenario")

class House(TimestampMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)
    interest: so.Mapped[int] = so.mapped_column(sa.Integer)
    loan_term: so.Mapped[int] = so.mapped_column(sa.Integer)
    buy_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Age.id))
    sell_at_age: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Age.id))

    #Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='houses')

    #Relationship to Scenario
    scenario: so.Mapped[list["ScenarioHouse"]] = so.relationship(back_populates="house")

    def __repr__(self):
        return '<House {}>'.format(self.name)
    
class ScenarioChild(db.Model):
    left_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("scenario.id"), primary_key=True)
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("child.id"), primary_key=True
    )
    born_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Age.id))
    independent_year: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Age.id))
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="child")
    child: so.Mapped["Child"] = so.relationship(back_populates="scenario")

class Child(TimestampMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    born_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Age.id))
    independent_year: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Age.id))

    #Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='children')

    #Relationship to Scenario
    scenario: so.Mapped[list["ScenarioChild"]] = so.relationship(back_populates="child")

    def __repr__(self):
        return '<Child {}>'.format(self.name)
    
# class Age(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     year: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

#     def __repr__(self):
#         return '<Age {} years>'.format(self.year)
