from flask import Flask, redirect, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'koom11'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():

    return redirect("/users")

@app.route("/users")
def users_index():

    users = User.query.all()
    return render_template("users/list.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():

    return render_template("users/new.html")

@app.route("/users/new",  methods=["POST"])
def add_new_user():

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    post = Post.query.all()
    return render_template("users/show.html", user=user, post=post)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/posts")
def get_posts():
    """Shows all posts by all users"""
    posts = Post.query.all()
    return render_template("blogPosts/show.html", posts=posts)

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Shows form for current user to create blog post"""
    user = User.query.get_or_404(user_id)
    return render_template("blogPosts/new_post.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")