import unittest
from app import app, db, User

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app to use the testing database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Create the database and the tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all the tables in the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_endpoint(self):
        # Simulate a POST request to /register to create a new user
        response = self.app.post('/register', data={
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password': 'testpassword'
        })
        # Check if the response is a redirect to the login page (status code 302)
        self.assertEqual(response.status_code, 302)

        # Check if the user was actually created in the database
        with app.app_context():
            user = User.query.filter_by(username='testuser1').first()
            self.assertIsNotNone(user)

    def test_login_endpoint(self):
        # First, create a user using the /register endpoint
        self.app.post('/register', data={
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'testpassword'
        })

        # Simulate a POST request to /login to log in the user
        response = self.app.post('/login', data={
            'username': 'testuser2',
            'password': 'testpassword'
        })
        # Check if the response is a redirect to the home page (status code 302)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
