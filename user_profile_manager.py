from models import db, User

class UserProfileManager:

    # Creating a user profile
    def create_user_profile(self, username, password, bio):
        user = User(username=username, password=password, bio=bio)
        db.session.add(user)
        db.session.commit()
        return user

    # Searching for a user by username
    def search_user(self, username):
        return User.query.filter(User.username.ilike(f'%{username}%')).all()

    # Deleting a user profile by username
    def delete_user_profile(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()

    # 5.2.1 Accept a friend request
    def accept_friend_request(self, requestor_id, user_id):
        requestor = User.query.get(requestor_id)
        user = User.query.get(user_id)
        if requestor and user:
            user.friends.append(requestor)  # Assuming `friends` is a relationship in the User model
            user.pending_requests.remove(requestor)  # Assuming `pending_requests` is a relationship
            db.session.commit()

    # 5.2.2 Reject a friend request
    def reject_friend_request(self, requestor_id, user_id):
        requestor = User.query.get(requestor_id)
        user = User.query.get(user_id)
        if requestor and user:
            user.pending_requests.remove(requestor)
            db.session.commit()

    # 5.2.4 Send a friend request
    def send_friend_request(self, user_id, requested_id):
        user = User.query.get(user_id)
        requested_user = User.query.get(requested_id)
        if user and requested_user:
            requested_user.pending_requests.append(user)  # Add to pending requests
            db.session.commit()
            return True
        return False

    # 5.2.5 Remove a friend
    def remove_friend(self, user_id, friend_id):
        user = User.query.get(user_id)
        friend = User.query.get(friend_id)
        if user and friend:
            user.friends.remove(friend)
            db.session.commit()

    # 5.2.6 View user profile
    def view_user_profile(self, user_profile_id):
        user_profile = User.query.get(user_profile_id)
        return user_profile

    # 5.3.1 Get profile bio
    def get_profile_bio(self, user_id):
        user = User.query.get(user_id)
        return user.bio if user else None

    # 5.3.2 Set profile bio
    def set_profile_bio(self, user_id, profile_bio):
        user = User.query.get(user_id)
        if user:
            user.bio = profile_bio
            db.session.commit()

    # 5.3.3 Get profile picture (assuming profile_picture is a file path in the User model)
    def get_profile_picture(self, user_id):
        user = User.query.get(user_id)
        return user.profile_picture if user else None

    # 5.3.4 Set profile picture
    def set_profile_picture(self, user_id, profile_picture):
        user = User.query.get(user_id)
        if user:
            user.profile_picture = profile_picture
            db.session.commit()

    # 5.3.5 Get personal records (PRs)
    def get_profile_prs(self, user_id):
        user = User.query.get(user_id)
        return user.prs if user else None

    # 5.3.6 Set personal records (PRs)
    def set_profile_prs(self, user_id, profile_prs):
        user = User.query.get(user_id)
        if user:
            user.prs = profile_prs
            db.session.commit()

    # 5.3.7 Get social media links
    def get_social_media_links(self, user_id):
        user = User.query.get(user_id)
        return user.social_media_links if user else None

    # 5.3.8 Set social media links
    def set_social_media_links(self, user_id, social_media_links):
        user = User.query.get(user_id)
        if user:
            user.social_media_links = social_media_links
            db.session.commit()

    # 5.3.9 Get user friends
    def get_user_friends(self, user_id):
        user = User.query.get(user_id)
        return user.friends if user else []

    # 5.3.10 Set user friends
    def set_user_friends(self, user_id, user_friends):
        user = User.query.get(user_id)
        if user:
            user.friends = user_friends
            db.session.commit()

    # 5.3.11 Get friend requests
    def get_friend_requests(self, user_id):
        user = User.query.get(user_id)
        return user.pending_requests if user else []

    # 5.3.12 Set friend requests
    def set_friend_requests(self, user_id, friend_requests):
        user = User.query.get(user_id)
        if user:
            user.pending_requests = friend_requests
            db.session.commit()

    # 5.3.13 Get group memberships
    def get_group_memberships(self, user_id):
        user = User.query.get(user_id)
        return user.groups if user else []

    # 5.3.14 Set group memberships
    def set_group_memberships(self, user_id, group_memberships):
        user = User.query.get(user_id)
        if user:
            user.groups = group_memberships
            db.session.commit()

    # 5.3.15 Get privacy settings
    def get_privacy_settings(self, user_id):
        user = User.query.get(user_id)
        return user.privacy_settings if user else None

    # 5.3.16 Set privacy settings
    def set_privacy_settings(self, user_id, privacy_settings):
        user = User.query.get(user_id)
        if user:
            user.privacy_settings = privacy_settings
            db.session.commit()

    # 5.3.17 Get unit preferences
    def get_unit_preferences(self, user_id):
        user = User.query.get(user_id)
        return user.unit_preferences if user else None

    # 5.3.18 Set unit preferences
    def set_unit_preferences(self, user_id, unit_preferences):
        user = User.query.get(user_id)
        if user:
            user.unit_preferences = unit_preferences
            db.session.commit()

    # 5.3.19 Get username
    def get_username(self, user_id):
        user = User.query.get(user_id)
        return user.username if user else None

    # 5.3.20 Set username
    def set_username(self, user_id, username):
        user = User.query.get(user_id)
        if user:
            user.username = username
            db.session.commit()

    # 5.3.21 Get password
    def get_password(self, user_id):
        user = User.query.get(user_id)
        return user.password if user else None

    # 5.3.22 Set password
    def set_password(self, user_id, password):
        user = User.query.get(user_id)
        if user:
            user.password = password
            db.session.commit()

    # 5.3.23 Get post history
    def get_post_history(self, user_id):
        user = User.query.get(user_id)
        return user.post_history if user else []

    # 5.3.24 Set post history
    def set_post_history(self, user_id, post_history):
        user = User.query.get(user_id)
        if user:
            user.post_history = post_history
            db.session.commit()

    # 5.3.25 Get workout history
    def get_workout_history(self, user_id):
        user = User.query.get(user_id)
        return user.workout_history if user else []

    # 5.3.26 Set workout history
    def set_workout_history(self, user_id, workout_history):
        user = User.query.get(user_id)
        if user:
            user.workout_history = workout_history
            db.session.commit()