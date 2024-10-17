from models import db, Post, User

class PostManager:
    def create_post(self, username, media_url, caption):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError("User does not exist")

        post = Post(user_id=user.id, content=caption, media_url=media_url)
        db.session.add(post)
        db.session.commit()
        return post

    def validate_upload(self, file_data):
        # Add logic to validate the upload based on your needs
        # For instance, check if it's an image/video by checking file headers
        return True