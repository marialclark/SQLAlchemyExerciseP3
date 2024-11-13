import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://i.postimg.cc/rmwyCQj9/default-avatar.png"

class User(db.Model):
    """Establishing User Class"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                            nullable=False)
    
    last_name = db.Column(db.String(50), 
                          nullable=False)
    
    image_url = db.Column(db.Text, 
                          nullable=False,
                          default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", 
                            backref="user", 
                            lazy=True, 
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    """Establishing Post Class"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(50), 
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)

    
class PostTag(db.Model):
    """Establishing PostTag Class"""
    __tablename__ = 'posts_tags'
    
    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True,
                        nullable=False)

    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True,
                       nullable=False)

class Tag(db.Model):
    """Establishing Tag Class"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    name = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    
    posts = db.relationship('Post',
                            secondary="posts_tags", 
                            backref="tags")

    
def connect_db(app):
    db.app = app
    db.init_app(app)