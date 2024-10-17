from models import db, User

class UserProfileManager:
    def create_user_profile(self, username, password, bio):
        user = User(username=username, password=password, bio=bio)
        db.session.add(user)
        db.session.commit()
        return user

    def search_user(self, username):
        return User.query.filter(User.username.ilike(f'%{username}%')).all()

    def delete_user_profile(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()