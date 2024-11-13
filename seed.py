"""Seed file to make sample data for db."""

from models import User, Post, Tag, db
from app import app
from datetime import datetime

# Create all tables
db.drop_all()
db.create_all()

maria = User(first_name="Maria", last_name="Clark", image_url="https://i.postimg.cc/9fKWGKR0/IMG-9585-copy.jpg")
channy = User(first_name="Chandler", last_name="Clark", image_url="https://i.postimg.cc/QMyGCVHW/channy.png")
duncan = User(first_name="Duncan", last_name="Clark", image_url="https://i.postimg.cc/g09RNS6S/IMG-0854.jpg")
mom = User(first_name="Cathlene", last_name="Clark")
dad = User(first_name="Thomas", last_name="Clark")
cassie = User(first_name="Cassie", last_name="Clark")
yo_momma = User(first_name="Yo", last_name="Momma")

db.session.add_all([maria, channy, duncan, mom, dad, cassie, yo_momma])
db.session.commit()

post1 = Post(title="Meow Meow", content="Meow, meow meow. Meow meow meow. 'Meow?' I meowed. 'Meow... meow. I'm meowy.' She responded.", created_at=datetime(2024, 11, 12, 16, 46, 1), user_id=channy.id)
post2 = Post(title="My Mom's Tuna Song", content="I love my mom's tuna song! I come running whenever she sings it.", created_at=datetime(2024, 11, 12, 16, 47, 2), user_id=channy.id)
post3 = Post(title="Chandler's Tuna Song", content="Tuna, tuna, Channy come get some tuna.", created_at=datetime(2024, 11, 12, 16, 48, 16), user_id=maria.id)
post4 = Post(title="I love fishing", content="I caught a huge fish today while fishing with my wife. It was awesome!", created_at=datetime(2024, 11, 12, 20, 59, 48), user_id=dad.id)
post5 = Post(title="What My Kids Say", content="That I am the best mom ever!!!!!", created_at=datetime(2024, 11, 12, 21, 7, 20), user_id=mom.id)
post6 = Post(title="Am I a Good Sister?", content="Yes I am!", created_at=datetime(2024, 11, 12, 21, 34, 41), user_id=cassie.id)
post7 = Post(title="Yo momma", content="Dane's butt crack!", created_at=datetime(2024, 11, 12, 21, 36, 34), user_id=yo_momma.id)

db.session.add_all([post1, post2, post3, post4, post5, post6, post7])
db.session.commit()

tag1 = Tag(name="Treats")
tag2 = Tag(name="Family")
tag3 = Tag(name="Fun")
tag4 = Tag(name="Fabulous")
tag5 = Tag(name="Hilarious")

db.session.add_all([tag1, tag2, tag3, tag4, tag5])
db.session.commit()

# Seed Posts_Tags relationships
post4.tags.extend([tag2, tag3, tag4])  # Tags for post ID 5
post5.tags.extend([tag2, tag3, tag4])  # Tags for post ID 6
post6.tags.extend([tag2, tag4])        # Tags for post ID 7
post7.tags.extend([tag2, tag5])        # Tags for post ID 8
post2.tags.extend([tag1, tag2, tag4])  # Tags for post ID 2

db.session.commit()