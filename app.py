from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "secretsarebad"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# BLOGLY ASSIGNMENT PART 1 ROUTES

@app.route('/')
def home_page():
    """Redirects to list of users"""
    return redirect("/users")


@app.route('/users')
def list_users():
    """Shows all users"""
    users = User.query.all()
    return render_template('user/list.html', users=users)


@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Loads form to create a new user"""
    return render_template('user/new.html')


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


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows details about a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('user/details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user(user_id):
    """Shows the edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('user/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def save_user(user_id):
    """Processes edit form and return user to /users"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# BLOGLY ASSIGNMENT PART 2 ROUTES 

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post(user_id):
    """Renders form for new user post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Handles add post form and redirects user to /users"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'], 
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post details"""
    post = Post.query.get_or_404(post_id)
    return render_template('post/details.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def edit_post(post_id):
    """Renders post edit form."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handles editing of a post and redirects back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

# BLOGLY ASSIGNMENT PART 3 ROUTES

@app.route('/tags')
def list_tags():
    """Renders tags list with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tag/list.html', tags=tags)


@app.route('/tags/new', methods=["GET"])
def new_tag_form():
    """Shows form to add a new tag"""
    # posts = Post.query.all()
    # return render_template('/tag/new.html', posts=posts)
    return render_template('/tag/new.html')


@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Processes add form, adds tag, and redirects to tag list."""
    name = request.form['name']

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Shows details about a tag. Has links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def edit_tag(tag_id):
    """Shows edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/edit.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def save_tag(tag_id):
    """Processes edit form, edits tag, and redirects to tag list."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deletes tag."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")