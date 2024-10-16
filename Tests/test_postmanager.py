# Test file for the PostManager class
# All of the imports here can be changed, I just don't know how things are laid out yet exactly.

import unittest
from app.post_manager import PostManager
from app.user_profile_manager import UserProfileManager


class TestMultimediaUpload(unittest.TestCase):

    def setUp(self):
        self.post_manager = PostManager()
        self.user_manager = UserProfileManager()
        self.user = self.user_manager.create_user_profile("testuser", "password", "bio")

    def test_upload_image(self):
        # Simulation of uploading an image
        image_data = b'imagebytes' # Not sure for this rn
        post = self.post_manager.create_post(self.user.username, image_data, caption="First Workout Pic")
        self.assertIsNotNone(post)
        self.assertEqual(post.username, "testuser")
        self.assertEqual(post.caption, "First Workout Pic")

    def test_upload_invalid_file(self):
        # Simulation of uploading an image type that is invalid
        invalid_data = b'imagebytes' # Not sure for this rn
        with self.assertRaises(ValueError):
            self.post_manager.create_post(self.user.username, invalid_data, caption = "Invalid File")

    def tearDown(self):
        # Clean up after tests, removing the post and user
        self.user_manager.delete_user_profile("testuser")

if __name__ == '__main__':
    unittest.main()