import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from exercise import Exercise
from models import db


class TestExercise(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app and test database
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        # Initialize an exercise for testing
        self.exercise = Exercise("Push-Up", 5, [0,0,0,0,0], [5,6,7,7,8])

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_set_reps(self):
        # Test setting reps
        self.exercise.exerciseSets = 15
        self.assertEqual(self.exercise.exerciseSets, 15)

    def test_set_invalid_weight(self):
        # Test setting an invalid weight
        with self.assertRaises(ValueError):
            self.exercise.exerciseWeights = "invalid_weight"  # Assuming weight should be numeric


if __name__ == "__main__":
    unittest.main()
