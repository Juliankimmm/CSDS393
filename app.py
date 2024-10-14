from flask import Flask
from Collegym.models import db, User, WorkoutLog, Group, Post
from Collegym.routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collegym.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)