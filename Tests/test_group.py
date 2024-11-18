import unittest
from app import app
from group_manager import GroupManager
from models import db
from user_profile_manager import UserProfileManager


class TestGroup(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        # Initialize managers and create a group for testing
        self.group_manager = GroupManager()
        self.user_manager = UserProfileManager()
        self.owner = self.user_manager.create_user_profile(
            "owner", "password", "Group Owner"
        )
        self.group = self.group_manager.create_group(self.owner.username, "Test Group")

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_member_to_group(self):
        # Test adding a new member to the group
        new_member = self.user_manager.create_user_profile(
            "newMember", "password", "bio"
        )
        result = self.group_manager.add_member(self.group.id, new_member.username)
        self.assertTrue(result)
        self.assertIn(new_member.username, self.group.members)


if __name__ == "__main__":
    unittest.main()
