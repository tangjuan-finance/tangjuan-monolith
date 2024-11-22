from datetime import datetime, timezone
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
    session,
)
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.main.forms import EditProfileForm, IndexAnonyServiceForm
from app.models import User
from app.main import bp
from app.lib import verify_signature
import git
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route("/update_server", methods=["POST"])
def webhook():
    W_SECRET = current_app.config["W_SECRET"]
    if request.method == "POST":
        signature_header = request.headers.get("X-Hub-Signature-256")
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        payload_body = request.data
        verify_signature(payload_body, W_SECRET, signature_header)

        payload = request.get_json()
        if payload is None:
            print("Deploy payload is empty: {payload}".format(payload=payload))
            # abort(abort_code)
            return "", 404

        if payload["ref"] != "refs/heads/main":
            return json.dumps({"msg": "Not main; ignoring"})
        repo = git.Repo("./f4lazylifes")
        origin = repo.remotes.origin

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({"msg": "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({"msg": "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f"{build_commit}")
        return "Updated PythonAnywhere server to commit {commit}".format(
            commit=commit_hash
        ), 200
    else:
        return "Wrong event type", 400


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    else:
        form = IndexAnonyServiceForm()
        if form.validate_on_submit():
            breakpoint()
            start_year = form.start_year.data
            expense_amount = form.expense_amount.data
            investment_amount = form.investment_amount.data
            salary_amount = form.salary_amount.data
            house_start_year = form.house_start_year.data
            house_amount = form.house_amount.data
            down_payment = form.down_payment.data
            interest = form.interest.data
            loan_term = form.loan_term.data
            child_born_at_age = form.child_born_at_age.data
            investment_ratio = form.investment_ratio.data
            retire_age = form.retire_age.data

            monthly_house_debt = (
                (house_amount - down_payment) * (1 + interest * 0.01)
            ) / (loan_term * 12)

            x = range(start_year, 86)
            y = list
            breakpoint()
            for this_year in x:
                if this_year >= retire_age:
                    salary_amount = 0

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
                investment_amount = investment_amount * 1.05 * saving
                y.append(investment_amount)

                salary_amount = salary_amount * 1.01
                expense_amount = expense_amount * 1.01
            breakpoint()
            # Generate the figure **without using pyplot**.
            fig = Figure()
            ax = fig.subplots()
            ax.plot(x, y)
            # Save it to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            session["data"] = data
            return redirect(url_for("main.index"))
        if "data" not in session:
            # Generate the figure **without using pyplot**.
            fig = Figure()
            ax = fig.subplots()
            ax.plot([1, 2], [5, 7])
            # Save it to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return render_template("index.html", form=form, data=data)


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
