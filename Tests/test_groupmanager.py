import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from group_manager import GroupManager
from models import db
from user_profile_manager import UserProfileManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestGroupCreationAndJoining(unittest.TestCase):

    def setUp(self):
        # Setup for Flask app and test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Using a test database
         # Push the application context
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()  # Create tables within this application context
        self.app = app.test_client()

        # Initialize managers and create test users
        self.group_manager = GroupManager()
        self.user_manager = UserProfileManager()
        self.user1 = self.user_manager.create_user_profile(
            "user1", "password1", "bio1")
        self.user2 = self.user_manager.create_user_profile(
            "user2", "password2", "bio2")

    def tearDown(self):
        # Clean up database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_group(self):
        # Testing Group Creation
        group = self.group_manager.create_group(self.user1.username, "Group 1")
        self.assertIsNotNone(group)
        self.assertEqual(group.group_name, "Group 1")
        self.assertIn(self.user1.username, group.members)

    def test_join_group(self):
        # Test joining a group
        group = self.group_manager.create_group(self.user1.username, "Group 1")
        result = self.group_manager.join_group(
            self.user2.username, group.group_id)
        self.assertTrue(result)
        self.assertIn(self.user2.username, group.members)

    def test_join_non_existent_group(self):
        # Testing trying to join a group that doesn't exist
        with self.assertRaises(ValueError):
            self.group_manager.join_group(self.user2.username, "fake-group-id")


if __name__ == "__main__":
    unittest.main()
