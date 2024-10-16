# Test file for the GroupManager class
# All of the imports here can be changed, I just don't know how things are laid out yet exactly.

import unittest
from app.user_profile_manager import UserProfileManager

class TestUserSearch(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserProfileManager()
        self.user1 = self.user_manager.create_user_profile("user1", "password1", "Bio1")
        self.user2 = self.user_manager.create_user_profile("user2", "password2", "Bio2")

    def test_search_user_by_username(self):
        # Basic testing of the search method
        result = self.user_manager.search_user("user1")
        self.assertIsNotNone(result)
        self.assertEqual(result.username, "user1")

    def test_search_user_partial_match(self):
        # Test partial matches of usernames
        results = self.user_manager.search_user("1")
        self.assertEqual(len(results), 1)
        usernames = [user.username for user in results]
        self.assertIn("user1", usernames)

    def test_search_nonexistent_user(self):
        # Test searching for a user that doesn't exist
        result = self.user_manager.search_user("user3")
        self.assertIsNone(result)

    def tearDown(self):
        self.user_manager.delete_user("user1")
        self.user_manager.delete_user("user2")

if __name__ == '__main__':
    unittest.main()