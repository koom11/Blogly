from flask import Flask, redirect, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User



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

@app.route("/user/new", methods=["GET"])
def new_user_form():

    return render_template("users/new.html")

