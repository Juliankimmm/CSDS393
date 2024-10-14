class NotificationManager:
    def __init__(self):
        self.notification_templates = {
            'workout_started': [
                "Your friend {username} has entered the gym!",
                "Your friend {username} is in the gym... Where are you?",
                "Your friend {username} is working out. Join them!"
            ],
            'friend_request': "{username} has sent you a friend request.",
            'group_invite': "{username} has invited you to join the group: {group_name}.",
            'post_activity': "{username} has posted new content."
        }

    def send_notification(self, notification_type, username, group_name=None):
        if notification_type in self.notification_templates:
            if isinstance(self.notification_templates[notification_type], list):
                for message in self.notification_templates[notification_type]:
                    print(message.format(username=username))
            else:
                message = self.notification_templates[notification_type].format(username=username, group_name=group_name)
                print(message)

class GroupWorkout:
    def __init__(self, group_name, exercises=None):
        self.group_name = group_name
        self.exercises = exercises if exercises else []
        self.participants = []

    def add_exercise(self, exercise_name, sets, reps, weight):
        self.exercises.append({
            'exercise_name': exercise_name,
            'sets': sets,
            'reps': reps,
            'weight': weight
        })

    def add_participant(self, username):
        self.participants.append(username)

    def display_workout_summary(self):
        print(f"Group Workout: {self.group_name}")
        for participant in self.participants:
            print(f"- {participant} is participating.")
        print("Workout Routine:")
        for exercise in self.exercises:
            print(f"{exercise['exercise_name']}: {exercise['sets']} sets, {exercise['reps']} reps, {exercise['weight']} kg")

class UserProfile:
    def __init__(self, username, bio="", prs=None, social_links=None):
        self.username = username
        self.bio = bio
        self.prs = prs if prs else {}
        self.social_links = social_links if social_links else {}

    def update_bio(self, new_bio):
        self.bio = new_bio

    def set_pr(self, lift_type, weight):
        self.prs[lift_type] = weight

    def add_social_link(self, platform, link):
        self.social_links[platform] = link

    def display_profile(self):
        print(f"User: {self.username}")
        print(f"Bio: {self.bio}")
        print("Personal Records (PRs):")
        for lift, weight in self.prs.items():
            print(f"{lift}: {weight} kg")
        print("Social Media Links:")
        for platform, link in self.social_links.items():
            print(f"{platform}: {link}")