"""Seed file for Blogly_db"""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

user1 = User(first_name="Eric", last_name="Kummer", image_url="")
user2 = User(first_name="Monty", last_name="Python", image_url="")
user3 = User(first_name="Holy", last_name="Hand Grenade", image_url="")
user4 = User(first_name="Razer", last_name="Naga", image_url="")

post1 = Post(title="", content="", created_at="")
post1 = Post(title="", content="", created_at="")
post1 = Post(title="", content="", created_at="")
post1 = Post(title="", content="", created_at="")