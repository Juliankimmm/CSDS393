from models import Post, User, db


class PostManager:
    def create_post(self, username, media_url, caption):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError("User does not exist")

        post = Post(user_id=user.id, content=caption, media_url=media_url)
        
        user.add_post(post)
        db.session.add(post)
        db.session.commit()

        return post

    def validate_upload(self, file_data):
        # Add logic to validate the upload based on your needs
        return True

    def display_post(self, postID):
        post = Post.query.get(postID)
        if not post:
            raise ValueError("Post does not exist")
        post_content = {"file": post.media_url, "caption": post.content}
        return post_content

    def display_user_info(self, postID):
        post = Post.query.get(postID)
        if not post:
            raise ValueError("Post does not exist")
        user = User.query.get(post.user_id)
        user_info = {
            "username": user.username,
            "profile_picture": user.profile_picture,  # Assuming 'profile_picture' exists
        }
        return user_info

    def like_post(self, postID, userID):
        post = Post.query.get(postID)
        user = User.query.get(userID)
        if not post or not user:
            raise ValueError("Post or User does not exist")
        if user.id not in post.likes:
            post.likes.append(user.id)
            db.session.commit()

    def remove_like(self, postID, userID):
        post = Post.query.get(postID)
        user = User.query.get(userID)
        if not post or not user:
            raise ValueError("Post or User does not exist")
        if user.id in post.likes:
            post.likes.remove(user.id)
            db.session.commit()

    def add_comment(self, postID, userID, comment):
        post = Post.query.get(postID)
        user = User.query.get(userID)
        if not post or not user:
            raise ValueError("Post or User does not exist")
        post.comments.append({"user_id": user.id, "comment": comment})
        db.session.commit()

    def remove_comment(self, postID, userID):
        post = Post.query.get(postID)
        if not post:
            raise ValueError("Post does not exist")
        post.comments = [
            comment for comment in post.comments if comment["user_id"] != userID
        ]
        db.session.commit()

    def delete_post(self, postID):
        post = Post.query.get(postID)
        if not post:
            raise ValueError("Post does not exist")
        db.session.delete(post)
        db.session.commit()

    def group_post(self, postID, groupID):
        post = Post.query.get(postID)
        if not post:
            raise ValueError("Post does not exist")
        post.group_id = groupID
        db.session.commit()

    def view_group_post(self, postID, groupID):
        post = Post.query.get(postID)
        if not post or post.group_id != groupID:
            raise ValueError("Post does not exist in the specified group")
        post_content = {"file": post.media_url, "caption": post.content}
        return post_content
