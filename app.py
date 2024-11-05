from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "secretsarebad"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """ Redirect to list of users"""
    return redirect("/users")

@app.route('/users')
def show_users():
    """Shows all users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
def load_create_user_form():
    """Loads form to create a new user"""
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Processes add form, adds new user and redirects back to /users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def get_user_details(user_id):
    """Shows details about a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    """Shows the edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_edited_user(user_id):
    """Processes edit form and return user to /users"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
    