import os
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for, current_app)
from werkzeug.utils import secure_filename
from models import Group, Post, User, WorkoutLog, GroupMembers, db
from user_profile_manager import UserProfileManager

main = Blueprint("main", __name__)
profile_manager = UserProfileManager()

# Default route that is displayed when the app is launched.
@main.route("/")
def index():
    return render_template("index.html")

# The update_preferences route handles the posting of settings not already covered by the profile route.
@main.route("/update_preferences/<int:user_id>", methods=["POST"])
def update_preferences(user_id):
    privacy_settings = request.form.get("privacy_settings")
    unit_preferences = request.form.get("unit_preferences")
    profile_manager.set_privacy_settings(user_id, privacy_settings)
    profile_manager.set_unit_preferences(user_id, unit_preferences)
    flash("Preferences updated successfully.")
    return redirect(url_for("main.profile", user_id=user_id))

# Handles the login page, both for its display and the accepting of information to direct the yser to their profile.
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.profile", user_id=user.id))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

# Handles the creation of accounts, taking in a username and a password.
@main.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["new-username"]
    password = request.form["new-password"]
    bio = request.form.get("bio", "")
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Username already exists", "danger")
        return redirect(url_for("main.login"))
    new_user = profile_manager.create_user_profile(username, password, bio)
    session["user_id"] = new_user.id
    flash("Account created successfully!", "success")
    return redirect(url_for("main.profile", user_id=new_user.id))

# Handles both the displaying and the altering of the profile page.
@main.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        flash("You need to log in first", "warning")
        return redirect(url_for("main.login"))
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        if "bio" in request.form:
            user.bio = request.form["bio"]
        if "pr" in request.form:
            user.pr = request.form["pr"]
        if "social_media" in request.form:
            user.social_media = request.form["social_media"]
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file.filename != "":
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                user.profile_picture = filename
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(request.url)

    workout_logs = WorkoutLog.query.filter_by(user_id=user_id).all()

    return render_template("profile.html", user=user, workout_logs=workout_logs)

# This route is for the workout log section of the app, and both displays and posts workout logs
@main.route("/workout_log/<int:user_id>", methods=["GET", "POST"])
def workout_log(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        flash("You need to login first", "warning")
        return redirect(url_for("main.login"))
    workout_logs = WorkoutLog.query.filter_by(user_id=user_id).order_by(WorkoutLog.timestamp.desc()).all()
    if request.method == "POST":
        user_id = session["user_id"]
        exercise = request.form["exercise"]
        reps = request.form["reps"]
        weight = request.form["weight"]
        rpe = request.form["rpe"]
        workout_log = WorkoutLog(
            user_id=user_id, exercise=exercise, reps=reps, weight=weight, rpe=rpe
        )
        db.session.add(workout_log)
        db.session.commit()
        return redirect(url_for("main.workout_log", user_id=user_id))
    return render_template("workout_log.html")

# The group route, which handles both the displaying of groups, and the creation of groups.
@main.route("/group/<int:user_id>", methods=["GET", "POST"])
def group(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        flash("You need to login first", "warning")
        return redirect(url_for("main.login"))
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        user_id = session['user_id']

        # Checking for duplicate names of groups:
        existing_group = Group.query.filter_by(name=name).first()
        if existing_group:
            flash('A group with this name already exists. Please choose a different name.', 'danger')
            return redirect(url_for('main.group', user_id=user_id))
        
        new_group = Group(name=name, description=description)
        db.session.add(new_group)
        db.session.flush()
        creator_membership = GroupMembers(group_id=new_group.id, user_id=user_id)
        db.session.add(creator_membership)
        db.session.commit()
        return redirect(url_for("main.group", user_id=user_id))
    user_groups = Group.query.join(GroupMembers, Group.id == GroupMembers.group_id) \
                              .filter((GroupMembers.user_id == user_id)) \
                              .all()
    return render_template("group.html", groups=user_groups)

# This route is used for the search feature over multiple pages.
@main.route("/search", methods=["GET"])
def search_users():
    search_query = request.args.get("query", "")
    if search_query:
        results = User.query.filter(
            User.username.ilike(f"%{search_query}%")).all()
        usernames = [user.username for user in results]
        return jsonify(usernames)
    return jsonify([])

# This route is used to add users to groups. Once the group leader searches for a user and clicks the Add Member button,
# it will add them to the group and display the group on their side
@main.route("/group/<int:group_id>/add_member", methods=["POST"])
def add_member(group_id):
    if "user_id" not in session:
        flash("You need to login first", "warning")
        return redirect(url_for("main.login"))
    user_id = session["user_id"]
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the user is already a member of the group
    existing_membership = GroupMembers.query.filter_by(group_id=group_id, user_id=user.id).first()
    if existing_membership:
        return jsonify({"error": "User is already a member of this group"}), 400

    new_membership = GroupMembers(group_id=group_id, user_id=user.id)
    db.session.add(new_membership)
    db.session.commit()

    return jsonify({"message": f"User {username} added to the group!"}), 200