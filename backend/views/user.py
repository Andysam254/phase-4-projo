from flask import jsonify, request, Blueprint, current_app
from models import db, User, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

user_bp = Blueprint("user_bp", __name__)

# Fetch users (with their jobs and applications)
@user_bp.route("/users", methods=["GET"])
def fetch_users():
    users = User.query.all()

    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'is_approved': user.is_approved,
            'is_admin': user.is_admin,
            'username': user.username,
            "jobs": [
                {
                    "id": job.id,
                    "title": job.title,
                    "description": job.description,
                    "is_active": job.is_active,
                    "created_at": job.created_at
                } for job in user.jobs
            ],
            "applications": [
                {
                    "id": application.id,
                    "cover_letter": application.cover_letter,
                    "status": application.status,
                    "applied_at": application.applied_at,
                    "job": {
                        "id": application.job.id,
                        "title": application.job.title
                    }
                } for application in user.applications
            ]
        })

    return jsonify(user_list)

# Add user (Register a new user)
@user_bp.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    
    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_username or check_email:
        return jsonify({"error": "Username/email exists"}), 406
    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Sending a welcome email
        try:
            msg = Message(
                subject="Welcome to the Freelance Job Board",
                sender=current_app.config["MAIL_DEFAULT_SENDER"],
                recipients=[email],
                body="Welcome to the Freelance Job Board! We're glad to have you join us."
            )
            current_app.extensions['mail'].send(msg)
        except Exception as e:
            current_app.logger.error(f"Error sending email: {e}")

        return jsonify({"msg": "User saved successfully!"}), 201

# Update user (Change user details, including approval or admin status)
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_users(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get('username', user.username)
        email = data.get('email', user.email)
        password = data.get('password', user.password)
        is_approved = data.get('is_approved', user.is_approved)
        is_admin = data.get('is_admin', user.is_admin)

        check_username = User.query.filter(User.username == username, User.id != user.id).first()
        check_email = User.query.filter(User.email == email, User.id != user.id).first()

        if check_username or check_email:
            return jsonify({"error": "Username/email exists"}), 406
        else:
            user.username = username
            user.email = email
            user.password = generate_password_hash(password) if password else user.password
            user.is_approved = is_approved
            user.is_admin = is_admin
            db.session.commit()
            return jsonify({"success": "Updated successfully"}), 201
    else:
        return jsonify({"error": "User doesn't exist!"}), 404

# Delete user (Remove a user)
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_users(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "User doesn't exist!"}), 404
