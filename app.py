from flask import Flask, redirect, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'koom11'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    """Show most recent 5 posts"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("blogPosts/home.html", posts=posts)

@app.errorhandler(404)
def pagr_not_found(e):
    """Show 404 Message"""
    return render_template('404.html'), 404

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
    flash(f"{user.full_name} has been destroyed")

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

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show specific post"""
    post = Post.query.get_or_404(post_id)
    return render_template('blogPosts/details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    """Shows edit post form"""
    post = Post.query.get_or_404(post_id)
    return render_template('blogPosts/post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle form submission to edit post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' fixed!")
    
    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def get_all_tags():
    """Show All Tags"""
    return render_template("tags/all_tags.html")

@app.route("/tags/new")
def new_tag_form():
    """Show New Tag Form"""
    posts = Post.query.all()
    return render_template("tags/new.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def create_new_tag():
    """Submits Form to Create New Tag"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"New Tag: '{new_tag.name}' created!")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def get_tag(tag_id):
    """Show Specific Tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("tags/show.html", tag=tag, posts=posts)