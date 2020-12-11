from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMG_URL = 'https://source.unsplash.com/Gv7xtQRtM3s/160x90'

class User(db.Model):
    """User Model"""
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False, unique=False)
    last_name = db.Column(db.String(15), nullable=False,unique=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMG_URL)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post. Users can create posts on Blogly"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return better formatted date and time"""
        return self.created_at.strftime("%a %b %#d  %Y, %#I:%M %p")


class Tag(db.Model):
    """Tag. A post can have many tags and a tag can be associated with many posts."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')


class PostTag(db.Model):
    """PostTag. Join table for Posts and Tags."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)