# Test file for the GroupManager class
# All of the imports here can be changed, I just don't know how things are laid out yet exactly.

import unittest
from app.group_manager import GroupManager
from app.user_profile_manager import UserProfileManager

class TestGroupCreationAndJoining(unittest.TestCase):

    def setUp(self):
        self.group_manager = GroupManager()
        self.user_manager = UserProfileManager()
        self.user1 = self.user_manager.create_user_profile("user1", "password1", "bio1")
        self.user2 = self.user_manager.create_user_profile("user2", "password2", "bio2")

    def test_create_group(self):
        # Testing Group Creation
        group = self.group_manager.create_group(self.user1.username, "Group 1")
        self.assertIsNotNone(group)
        self.assertEqual(group.group_name, "Group 1")
        self.assertIn(self.user1.username, group.members)

    def test_join_group(self):
        # Test joining a group
        group = self.group_manager.create_group(self.user1.username, "Group 1")
        result = self.group_manager.join_group(self.user2.username, group.group_id)
        self.assertTrue(result)
        self.assertIn(self.user2.username, group.members)

    def test_join_non_existent_group(self):
        # Testing trying to join a group that isn't real
        with self.assertRaises(ValueError):
            self.group_manager.join_group(self.user2.username, "fake-group-id")

    def tearDown(self):
        # Cleaning up test user profiles
        self.user_manager.delete_user_profile("user1")
        self.user_manager.delete_user_profile("user2")

if __name__ == '__main__':
    unittest.main()