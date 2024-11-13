import unittest
from app import app, db
from models import User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

class BloglyAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down test database"""
        db.drop_all()

    def setUp(self):
        """Clear any existing data, set up test client, add test data"""
        db.session.execute('DELETE FROM posts_tags')
        db.session.commit()

        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        
        self.client = app.test_client()

        # Test User
        user = User(first_name="Test", last_name="User", image_url=None)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        # Test Tag
        tag = Tag(name="Test Tag")
        db.session.add(tag)
        db.session.commit()
        self.tag_id = tag.id

        # Test post associated with tag
        post = Post(title="Test Post", content="This is a test post.", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

        # Associate tag with post
        post_tag = PostTag(post_id=self.post_id, tag_id=self.tag_id)
        db.session.add(post_tag)
        db.session.commit()

    def tearDown(self):
        """Roll back any failed transactions"""
        db.session.rollback()

    def test_home_page(self):
        """Test home page redirect to /users"""
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertIn('/users', response.location)

    def test_show_users(self):
        """Test users listing page displays added user"""
        with self.client as client:
            response = client.get('/users')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)

    def test_load_create_user_form(self):
        """Test create user form loads correctly"""
        with self.client as client:
            response = client.get('/users/new')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Create New User', response.data)

    def test_create_user(self):
        """Test form submission creates new user and redirects"""
        with self.client as client:
            response = client.post('/users/new', data={
                'first_name': 'John',
                'last_name': 'Doe',
                'image_url': ''
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'John Doe', response.data)

    def test_user_details(self):
        """Test user details page displays correct user information"""
        with self.client as client:
            response = client.get(f'/users/{self.user_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)

    def test_create_post(self):
        """Test creating a new post for a user"""
        with self.client as client:
            response = client.post(f'/users/{self.user_id}/posts/new', data={
                'title': 'New Post',
                'content': 'This is a new post'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New Post', response.data)

    def test_delete_post(self):
        """Test deleting a post"""
        with self.client as client:
            response = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(Post.query.get(self.post_id))

    def test_edit_post(self):
        """Test editing a post"""
        with self.client as client:
            response = client.post(f'/posts/{self.post_id}/edit', data={
                'title': 'Updated Post',
                'content': 'Updated content for the post'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            updated_post = Post.query.get(self.post_id)
            self.assertEqual(updated_post.title, 'Updated Post')
        self.assertEqual(updated_post.content, 'Updated content for the post')

    def test_get_post_details(self):
        """Test viewing a post's details"""
        with self.client as client:
            response = client.get(f'/posts/{self.post_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Post', response.data)

    def test_edit_user(self):
        """Test form submission updates user and redirects"""
        with self.client as client:
            response = client.post(f'/users/{self.user_id}/edit', data={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'image_url': ''
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Jane Doe', response.data)

    def test_delete_user(self):
        """Test deleting a user"""
        with self.client as client:
            response = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(User.query.get(self.user_id))

    # TESTS FOR BLOGLY PART 3

    def test_list_tags(self):
        """Test the /tags page displays all tags"""
        with self.client as client:
            response = client.get('/tags')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Tag', response.data)

    def test_load_create_tag_form(self):
        """Test the /tags/new form loads correctly"""
        with self.client as client:
            response = client.get('/tags/new')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Create a Tag', response.data)

    def test_create_tag(self):
        """Test the tag creation form and redirect to /tags"""
        with self.client as client:
            response = client.post('/tags/new', data={
                'name': 'New Tag'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New Tag', response.data)

    def test_show_tag(self):
        """Test the /tags/<tag_id> page shows tag details"""
        with self.client as client:
            response = client.get(f'/tags/{self.tag_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Tag', response.data)

    def test_edit_tag(self):
        """Test loading the tag edit form and updating the tag"""
        with self.client as client:
            response = client.get(f'/tags/{self.tag_id}/edit')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Edit Tag', response.data)

            response = client.post(f'/tags/{self.tag_id}/edit', data={
                'name': 'Updated Tag'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Updated Tag', response.data)

    def test_delete_tag(self):
        """Test deleting a tag"""
        with self.client as client:
            response = client.post(f'/tags/{self.tag_id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(Tag.query.get(self.tag_id))

if __name__ == '__main__':
    unittest.main()
