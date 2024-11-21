from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.main.forms import EditProfileForm
from app.models import User
from app.main import bp
from app.lib import verify_signature
import git
import json


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
        return render_template("index.html", title="Home")


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
