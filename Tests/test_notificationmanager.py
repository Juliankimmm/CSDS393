import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from models import db
from notification_manager import NotificationManager
from user_profile_manager import UserProfileManager


class TestNotificationManager(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        # Initialize managers and create test users
        self.notification_manager = NotificationManager()
        self.user_manager = UserProfileManager()
        self.sender = self.user_manager.create_user_profile("sender", "password", "Notification Sender")
        self.receiver = self.user_manager.create_user_profile("receiver", "password", "Notification Receiver")

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_send_notification(self):
        # Test sending a notification
        result = self.notification_manager.send_notification(self.sender.username, self.receiver.username, "Workout session tomorrow!")
        self.assertTrue(result)

    def test_send_invalid_notification(self):
        # Test sending an invalid notification
        with self.assertRaises(ValueError):
            self.notification_manager.send_notification(self.sender.username, "nonexistent_user", "Invalid notification")


if __name__ == '__main__':
    unittest.main()