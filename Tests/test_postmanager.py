import unittest

from app import app
from models import db
from post_manager import PostManager
from user_profile_manager import UserProfileManager

class TestMultimediaUpload(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        # Initialize managers and create a test user
        self.post_manager = PostManager()
        self.user_manager = UserProfileManager()
        self.user = self.user_manager.create_user_profile("testuser", "password", "bio")

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_image(self):
        # Simulate uploading an image
        image_data = b"imagebytes"  # In a real case, this would be actual image data
        post = self.post_manager.create_post(
            self.user.username, image_data, caption="First Workout Pic"
        )
        self.assertIsNotNone(post)
        self.assertEqual(post.username, "testuser")
        self.assertEqual(post.caption, "First Workout Pic")

    def test_upload_invalid_file(self):
        # Simulate uploading an invalid file
        invalid_data = b"notanimage"
        with self.assertRaises(ValueError):
            self.post_manager.create_post(
                self.user.username, invalid_data, caption="Invalid File"
            )

if __name__ == "__main__":
    unittest.main()
