from app.api import bp
from app.api.errors import ValidationError

from flask import request, jsonify, url_for
from app import db
from app.models import User
import sqlalchemy as sa

from app.api.utils.encryption import encrypt_data
from app.api.utils.validation import validate_username, validate_email, validate_token
from app.api.services.redis_service import save_session_token
from app.api.services.email_service import send_email


# from app.api.services.email_service import send_email
# from app.api.services.redis_service import save_session_token, get_session_token

# @bp.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for("main.index"))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = db.session.scalar(
#             sa.select(User).where(User.username == form.username.data)
#         )
#         if user is None or not user.check_password(form.password.data):
#             flash("使用者名稱或密碼錯誤")
#             return redirect(url_for("auth.login"))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get("next")
#         if not next_page or urlsplit(next_page).netloc != "":
#             next_page = url_for("main.index")
#         return redirect(next_page)
#     return render_template("auth/login.html", title=("Sign In"), form=form)


# @bp.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("main.index"))


@bp.route("/register", methods=["POST"])
def create_registration():
    """Step 1: Receive email and send registration link."""
    email = request.json.get("email")
    if not email:
        # Raise a BadRequest with a custom error message
        raise ValidationError(errors={"email": "Email is required."})

    # Validate the email
    validate_email(email)
    # Encrypt a registration token
    token = encrypt_data({"email": email})
    register_url = url_for("api_v1.complete_registration", token=token, _external=True)

    # Only for dev, should delete later
    print("register_url: " + register_url)
    # Send email
    send_email(
        email, "Complete Your Registration", f"Click here to register: {register_url}"
    )

    return jsonify({"message": "Registration email sent"}), 200


@bp.route("/register/<token>", methods=["POST"])
def complete_registration(token):
    """Step 2: Register the user with username and password."""
    # Validate the token
    data = validate_token(token)

    username = request.json.get("username")
    password = request.json.get("password")
    # Check if both username and password provided
    if not username or not password:
        raise ValidationError(message="Username and password are required")

    # Validate the username
    validate_username(username)

    # Create user
    new_user = User(email=data["email"], username=username)
    new_user.set_password(password)

    # Save user to database
    db.session.add(new_user)
    db.session.commit()
    verified_user = db.session.scalar(
        sa.select(User).where(User.username == new_user.username)
    )
    # Generate session token and save to Redis
    session_token = encrypt_data({"userid": verified_user.id})
    session_id = save_session_token(session_token)

    # Return session ID to frontend
    return jsonify(
        {
            "message": "Registration successful",
            "payload": {"session_id": session_id},
        }
    ), 200
