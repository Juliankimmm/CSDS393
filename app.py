import os

from flask import Flask

from models import Group, GroupMembers, Post, User, WorkoutLog, db
from routes import main

app = Flask(__name__)

# Set configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URI", "sqlite:///test.db")
# Disable modification tracking
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_secret_key")

# Initialize database
db.init_app(app)

# Create tables only if the database file doesn't already exist
if not os.path.exists("test.db"):
    with app.app_context():
        db.create_all()

# Register Blueprints
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
