from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime




metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # Used to approve users for job applications
    is_admin = db.Column(db.Boolean, default=False)  # Admin privileges for managing users and jobs

    jobs = db.relationship("Job", backref="user", lazy=True)  # One-to-many relationship: user can post multiple jobs
    applications = db.relationship("Application", backref="user", lazy=True)  # One-to-many relationship: user can apply for many jobs

    def __repr__(self):
        return f'<User {self.username}>'

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Indicates if the job is still open for applications
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)  # Removed tag_id and replaced with deadline for simplicity
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 

    applications = db.relationship("Application", backref="job", lazy=True)  # One-to-many relationship: job can have many applications

    def __repr__(self):
        return f'<Job {self.title}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover_letter = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending") 
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)  

    def __repr__(self):
        return f'<Application {self.id}>'

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'