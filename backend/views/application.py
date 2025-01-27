from flask import jsonify, request, Blueprint
from models import db, Application, Job, User
from flask_jwt_extended import jwt_required, get_jwt_identity

application_bp = Blueprint("application_bp", __name__)

# ==================================APPLICATION======================================

# Add application (Freelancer applying for a job)
@application_bp.route("/applications", methods=["POST"])
@jwt_required()
def add_application():
    data = request.get_json()
    job_id = data['job_id']
    cover_letter = data['cover_letter']

    # Get current user ID (freelancer)
    user_id = get_jwt_identity()

    # Check if job exists
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    # Create new application
    new_application = Application(job_id=job_id, user_id=user_id, cover_letter=cover_letter)
    db.session.add(new_application)
    db.session.commit()
    return jsonify({"success": "Application submitted successfully"}), 201

# READ - Get all applications for the current user (Freelancer's Applications)
@application_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_user_applications():
    user_id = get_jwt_identity()

    applications = Application.query.filter_by(user_id=user_id).all()
    application_list = [
        {
            "id": application.id,
            "job_id": application.job_id,
            "job_title": application.job.title,
            "cover_letter": application.cover_letter,
            "status": application.status,
            "date_applied": application.date_applied
        } for application in applications
    ]
    return jsonify(application_list), 200

# READ - Get application by ID (for the current user)
@application_bp.route("/applications/<int:application_id>", methods=["GET"])
@jwt_required()
def get_application(application_id):
    user_id = get_jwt_identity()

    application = Application.query.filter_by(id=application_id, user_id=user_id).first()
    if not application:
        return jsonify({"error": "Application not found or unauthorized"}), 404

    application_details = {
        "id": application.id,
        "job_id": application.job_id,
        "cover_letter": application.cover_letter,
        "status": application.status,
        "date_applied": application.date_applied,
        "job_title": application.job.title
    }
    return jsonify(application_details), 200

# UPDATE - Update application details (e.g., cover letter or status)
@application_bp.route("/applications/<int:application_id>", methods=["PUT"])
@jwt_required()
def update_application(application_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    cover_letter = data.get('cover_letter')
    status = data.get('status')

    application = Application.query.get(application_id)
    if not application or application.user_id != user_id:
        return jsonify({"error": "Application not found or unauthorized"}), 404

    # Update application details
    if cover_letter:
        application.cover_letter = cover_letter
    if status:
        application.status = status

    db.session.commit()
    return jsonify({"success": "Application updated successfully"}), 200

# DELETE - Delete application
@application_bp.route("/applications/<int:application_id>", methods=["DELETE"])
@jwt_required()
def delete_application(application_id):
    user_id = get_jwt_identity()

    application = Application.query.filter_by(id=application_id, user_id=user_id).first()
    if not application:
        return jsonify({"error": "Application not found or unauthorized"}), 404

    db.session.delete(application)
    db.session.commit()
    return jsonify({"success": "Application deleted successfully"}), 200
