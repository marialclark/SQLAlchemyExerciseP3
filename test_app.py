import unittest
from app import app, db
from models import User

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
        """Clear any existing data, set up test client, add test user"""
        User.query.delete()
        db.session.commit()
        self.client = app.test_client()
        
        user = User(first_name="Test", last_name="User", image_url=None)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

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

if __name__ == '__main__':
    unittest.main()
