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

    # Accepting a friend request
    def accept_friend_request(self, requestor_id, user_id):
        requestor = User.query.get(requestor_id)
        user = User.query.get(user_id)
        if requestor and user:
            user.friends.append(requestor)  # Assuming `friends` is a relationship in the User model
            user.pending_requests.remove(requestor)  # Assuming `pending_requests` is a relationship
            db.session.commit()

    # Rejecting a friend request
    def reject_friend_request(self, requestor_id, user_id):
        requestor = User.query.get(requestor_id)
        user = User.query.get(user_id)
        if requestor and user:
            user.pending_requests.remove(requestor)
            db.session.commit()

    # Sending a friend request
    def send_friend_request(self, user_id, requested_id):
        user = User.query.get(user_id)
        requested_user = User.query.get(requested_id)
        if user and requested_user:
            requested_user.pending_requests.append(user)  # Add to pending requests
            db.session.commit()
            return True
        return False

    # Removing a friend
    def remove_friend(self, user_id, friend_id):
        user = User.query.get(user_id)
        friend = User.query.get(friend_id)
        if user and friend:
            user.friends.remove(friend)
            db.session.commit()

    # Viewing user profile
    def view_user_profile(self, user_profile_id):
        return User.query.get(user_profile_id)

    # Getting and setting various profile fields
    def get_profile_bio(self, user_id):
        user = User.query.get(user_id)
        return user.bio if user else None

    def set_profile_bio(self, user_id, profile_bio):
        user = User.query.get(user_id)
        if user:
            user.bio = profile_bio
            db.session.commit()

    def get_profile_picture(self, user_id):
        user = User.query.get(user_id)
        return user.profile_picture if user else None

    def set_profile_picture(self, user_id, profile_picture):
        user = User.query.get(user_id)
        if user:
            user.profile_picture = profile_picture
            db.session.commit()

    def get_profile_prs(self, user_id):
        user = User.query.get(user_id)
        return user.prs if user else None

    def set_profile_prs(self, user_id, profile_prs):
        user = User.query.get(user_id)
        if user:
            user.prs = profile_prs
            db.session.commit()

    def get_social_media_links(self, user_id):
        user = User.query.get(user_id)
        return user.social_media_links if user else None

    def set_social_media_links(self, user_id, social_media_links):
        user = User.query.get(user_id)
        if user:
            user.social_media_links = social_media_links
            db.session.commit()

    def get_user_friends(self, user_id):
        user = User.query.get(user_id)
        return user.friends if user else []

    def set_user_friends(self, user_id, user_friends):
        user = User.query.get(user_id)
        if user:
            user.friends = user_friends
            db.session.commit()

    def get_friend_requests(self, user_id):
        user = User.query.get(user_id)
        return user.pending_requests if user else []

    def set_friend_requests(self, user_id, friend_requests):
        user = User.query.get(user_id)
        if user:
            user.pending_requests = friend_requests
            db.session.commit()

    def get_group_memberships(self, user_id):
        user = User.query.get(user_id)
        return user.groups if user else []

    def set_group_memberships(self, user_id, group_memberships):
        user = User.query.get(user_id)
        if user:
            user.groups = group_memberships
            db.session.commit()

    def get_privacy_settings(self, user_id):
        user = User.query.get(user_id)
        return user.privacy_settings if user else None

    def set_privacy_settings(self, user_id, privacy_settings):
        user = User.query.get(user_id)
        if user:
            user.privacy_settings = privacy_settings
            db.session.commit()

    def get_unit_preferences(self, user_id):
        user = User.query.get(user_id)
        return user.unit_preferences if user else None

    def set_unit_preferences(self, user_id, unit_preferences):
        user = User.query.get(user_id)
        if user:
            user.unit_preferences = unit_preferences
            db.session.commit()