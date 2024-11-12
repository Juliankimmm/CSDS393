import unittest
from app import app
from models import db
from exercise import Exercise


class TestExercise(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        # Initialize an exercise for testing
        self.exercise = Exercise("Push-Up", reps=10, sets=3, weight=0)

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_set_reps(self):
        # Test setting reps
        self.exercise.reps = 15
        self.assertEqual(self.exercise.reps, 15)

    def test_set_invalid_weight(self):
        # Test setting an invalid weight
        with self.assertRaises(ValueError):
            self.exercise.weight = "invalid_weight"  # Assuming weight should be numeric


if __name__ == '__main__':
    unittest.main()