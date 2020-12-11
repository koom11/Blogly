"""Seed file for Blogly_db"""

from models import User, Post, db, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

user1 = User(first_name="Eric", last_name="Kummer")
user2 = User(first_name="Monty", last_name="Python")
user3 = User(first_name="Holy", last_name="Hand Grenade")
user4 = User(first_name="Razer", last_name="Naga")

post1 = Post(title="", content="", created_at="")
post1 = Post(title="", content="", created_at="")
post1 = Post(title="", content="", created_at="")
post1 = Post(title="", content="", created_at="")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.commit()
