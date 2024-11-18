import unittest

from app import app
from models import db
from user_profile_manager import UserProfileManager
from workout_log_manager import WorkoutLogManager

class TestWorkoutLogManager(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        # Initialize managers and create a test user
        self.workout_log_manager = WorkoutLogManager()
        self.user_manager = UserProfileManager()
        self.user = self.user_manager.create_user_profile(
            "workoutUser", "password", "workout bio"
        )

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_workout_log(self):
        # Test creating a workout log
        workout_log = self.workout_log_manager.create_workout_log(
            self.user.username, "Cardio Session"
        )
        self.assertIsNotNone(workout_log)
        self.assertEqual(workout_log.username, "workoutUser")
        self.assertEqual(workout_log.description, "Cardio Session")

    def test_delete_workout_log(self):
        # Test deleting a workout log
        workout_log = self.workout_log_manager.create_workout_log(
            self.user.username, "Cardio Session"
        )
        result = self.workout_log_manager.delete_workout_log(workout_log.id)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
