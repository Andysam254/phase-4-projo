from flask import jsonify, request, Blueprint
from models import db, User, Job, Application
from flask_jwt_extended import jwt_required, get_jwt_identity

job_bp = Blueprint("job_bp", __name__)

# ==================================JOB======================================

# Add Job
@job_bp.route("/job/add", methods=["POST"])
@jwt_required()
def add_job():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    title = data['title']
    description = data['description']
    deadline = data['deadline']  # Removed tag_id from data

    new_job = Job(title=title, description=description, user_id=current_user_id, deadline=deadline)
    db.session.add(new_job)
    db.session.commit()
    return jsonify({"success": "Job added successfully"}), 201

# Get All Jobs (User's jobs)
@job_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    current_user_id = get_jwt_identity()

    jobs = Job.query.filter_by(user_id=current_user_id)

    job_list = [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "user_id": job.user_id,
            "is_active": job.is_active,
            "deadline": job.deadline,
            "user": {"id": job.user.id, "username": job.user.username, "email": job.user.email}
        } for job in jobs
    ]

    return jsonify(job_list), 200

# Get Job by ID
@job_bp.route("/job/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):
    current_user_id = get_jwt_identity()

    job = Job.query.filter_by(id=job_id, user_id=current_user_id).first()
    if job:
        job_details = {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "user_id": job.user_id,
            "deadline": job.deadline
        }
        return jsonify(job_details), 200
    else:
        return jsonify({"error": "Job not found"}), 404

# Update Job
@job_bp.route("/job/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    current_user_id = get_jwt_identity()

    data = request.get_json()
    job = Job.query.get(job_id)

    if job and job.user_id == current_user_id:
        title = data.get('title', job.title)
        description = data.get('description', job.description)
        is_active = data.get('is_active', job.is_active)
        deadline = data.get('deadline', job.deadline)

        # Apply updates
        job.title = title
        job.description = description
        job.deadline = deadline
        job.is_active = is_active

        db.session.commit()
        return jsonify({"success": "Job updated successfully"}), 200
    else:
        return jsonify({"error": "Job not found/Unauthorized"}), 404

# Delete Job
@job_bp.route("/job/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    current_user_id = get_jwt_identity()

    job = Job.query.filter_by(id=job_id, user_id=current_user_id).first()

    if not job:
        return jsonify({"error": "Job not found/Unauthorized"}), 404

    db.session.delete(job)
    db.session.commit()
    return jsonify({"success": "Job deleted successfully"}), 200
