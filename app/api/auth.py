from app.api import bp
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from app import db
from app.models import User

# from app.api.utils.encryption import encrypt_data, decrypt_data
from app.api.utils.encryption import decrypt_data
from app.api.utils.validation import validate_username, validate_email
from cryptography.fernet import InvalidToken

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
        return jsonify({"error": "Email is required"}), 400

    try:
        # Validate the email
        validate_email(email)

        # Encrypt a registration token
        # token = encrypt_data({"email": email})
        # register_url = url_for("api_v1.complete_registration", token=token, _external=True)
        # Send email
        # send_email(email, "Complete Your Registration", f"Click here to register: {register_url}")

        return jsonify({"message": "Registration email sent"}), 200

    except BadRequest as e:
        # Return error messages as JSON response
        return jsonify({"error": str(e)}), 400


@bp.route("/register/<token>", methods=["POST"])
def complete_registration(token):
    """Step 2: Register the user with username and password."""
    try:
        data = decrypt_data(token)

        username = request.json.get("username")
        password = request.json.get("password")
        breakpoint()
        # Check if both username and password provided
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Validate the username
        validate_username(username)

        # Create user
        new_user = User(email=data["email"], username=username)
        new_user.set_password(password)

        # Save user to database
        db.session.add(new_user)
        db.session.commit()

        # Generate session token and save to Redis
        # session_token = encrypt_data({"userid": new_user.id})
        # session_id = save_session_token(session_token)

        # Return session ID to frontend
        return jsonify(
            {
                "message": "Registration successful",
                # "payload": {"session_id": session_id},
            }
        ), 200

    except InvalidToken:
        return jsonify({"error": "Invalid or expired token"}), 400
    except BadRequest as e:
        # Return error messages as JSON response
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Optionally log unexpected exceptions for debugging
        bp.logger.error(f"Unexpected error during token decryption: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
