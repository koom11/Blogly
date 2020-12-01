from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMG_URL = '<i class="fas fa-pen-alt"></i>'

class User(db.Model):
    """User Model"""
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False, unique=False)
    last_name = db.Column(db.String(15), nullable=False,unique=False)
    image_url = db.Column(db.String, default='<i class="fas fa-pen-alt"></i>')

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
