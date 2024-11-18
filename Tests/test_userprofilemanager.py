# Test file for the GroupManager class
# All of the imports here can be changed, I just don't know how things are laid out yet exactly.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from models import db
from user_profile_manager import UserProfileManager


class TestUserSearch(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.app = app.test_client()

        #with app.app_context():
         #   db.create_all()

        # Initialize the user manager and create test users
        self.user_manager = UserProfileManager()
        self.user1 = self.user_manager.create_user_profile("user1", "password1", "Bio1")
        self.user2 = self.user_manager.create_user_profile("user2", "password2", "Bio2")

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_search_user_by_username(self):
        # Test exact match for username
        result = self.user_manager.search_user("user1")
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "user1")

    def test_search_user_partial_match(self):
        # Test partial match of usernames
        results = self.user_manager.search_user("1")
        self.assertEqual(len(results), 1)
        usernames = [user.username for user in results]
        self.assertIn("user1", usernames)

    def test_search_nonexistent_user(self):
        # Test search for a user that does not exist
        result = self.user_manager.search_user("user3")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()