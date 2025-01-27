from flask import jsonify, request, Blueprint
from models import db, User, TokenBlocklist
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth_bp", __name__)

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# Get current user
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "email": user.email,
        "is_approved": user.is_approved,
        "is_admin": user.is_admin,
        "username": user.username,
        "user_type": "Freelancer" if user.is_freelancer else "Client"  # Added user type
    }

    return jsonify(user_data)

# Logout
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"success": "Logged out successfully"}), 200
