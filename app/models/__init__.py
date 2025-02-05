from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .event import Event
from .participation import Participation
from .review import Review