from dotenv import load_dotenv
from flask import Flask
from .config import Config
from .models import db
from .routes import register_routes
from .routes import jwt
from flask_migrate import Migrate

load_dotenv()

def create_app():
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    return app