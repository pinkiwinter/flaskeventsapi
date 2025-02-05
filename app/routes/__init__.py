from app.routes.auth import register_bp, login_bp
from app.routes.account import account__bp
from app.routes.events import events_bp
from app.routes.admin import admin_bp
from app.routes.participations import participation_bp
from app.routes.reviews import review_bp
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def register_routes(app):
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(account__bp)
    app.register_blueprint(participation_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(review_bp)
    

    