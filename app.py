import os
from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import main

def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Set configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", "sqlite:///test.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_secret_key")

    # Initialize database and migrations
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(main)

    return app

collegym = create_app()

if __name__ == "__main__":
    collegym.run(debug=True)