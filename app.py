from flask import Flask
from flask_migrate import Migrate
import sys
print(sys.path)
from models import db, User, WorkoutLog, Group, Post, GroupMembers  # Models import
from routes import main

app = Flask(__name__)

# Set up your database URI and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Change this to your actual DB URI
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration extensions
db.init_app(app)
migrate = Migrate(app, db)  # Set up Flask-Migrate

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)