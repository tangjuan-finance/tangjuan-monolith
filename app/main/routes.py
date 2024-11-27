from datetime import datetime, timezone
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.main.forms import EditProfileForm, IndexAnonyServiceForm
from app.models import User
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    else:
        form = IndexAnonyServiceForm()
        return render_template("index.html", form=form)


@bp.route("/process", methods=["GET", "POST"])
def process():
    # Receive Data
    input_data = request.json
    # Init
    start_year = input_data["start_year"]
    expense_amount = input_data["expense_amount"]
    investment_amount = input_data["investment_amount"]
    salary_amount = input_data["salary_amount"]
    house_start_year = input_data["house_start_year"]
    house_amount = input_data["house_amount"]
    down_payment = input_data["down_payment"]
    interest = input_data["interest"]
    loan_term = input_data["loan_term"]
    child_born_at_age = input_data["child_born_at_age"]
    investment_ratio = input_data["investment_ratio"]
    retire_age = input_data["retire_age"]

    monthly_house_debt = ((house_amount - down_payment) * (1 + interest * 0.01)) / (
        loan_term * 12
    )

    data = list()
    # Calculation
    for this_year in range(start_year, 86):
        if this_year >= retire_age:
            salary_amount = 0

        if this_year == house_start_year:
            investment_amount -= down_payment

        left = salary_amount - expense_amount

        pay_houst_debt = (this_year >= house_start_year) & (
            this_year < house_start_year + loan_term
        )
        if pay_houst_debt:
            left = left - monthly_house_debt

        raise_child = (this_year >= child_born_at_age) & (
            this_year < child_born_at_age + 22
        )
        if raise_child:
            left = left - 15000

        saving = left * investment_ratio * 0.01

        # Update
        investment_amount = investment_amount * 1.05 + saving
        data.append({"x": this_year, "y": round(investment_amount)})

        salary_amount = salary_amount * 1.01
        expense_amount = expense_amount * 1.01
    return {"data": data}


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@bp.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template("user.html", user=user)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("變更已儲存！")
        return redirect(url_for("main.user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)
