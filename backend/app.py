from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from datetime import timedelta
from models import db, TokenBlocklist

mail = Mail()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configure CORS
    CORS(app)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Configure Flask-Mail
    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = "andygitau444@gmail.com"
    app.config["MAIL_PASSWORD"] = "andygitau21768062"
    app.config["MAIL_DEFAULT_SENDER"] = "andygitau444@gmail.com"
    mail.init_app(app)

    # Configure JWT
    app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # Import and register blueprints here
    from views import user_bp, job_bp, application_bp, auth_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(auth_bp)

    return app
