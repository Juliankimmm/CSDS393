import os
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for, current_app)
from werkzeug.utils import secure_filename
from models import Group, Post, User, WorkoutLog, GroupMembers, db
from user_profile_manager import UserProfileManager

main = Blueprint("main", __name__)
profile_manager = UserProfileManager()


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/update_preferences/<int:user_id>", methods=["POST"])
def update_preferences(user_id):
    privacy_settings = request.form.get("privacy_settings")
    unit_preferences = request.form.get("unit_preferences")
    profile_manager.set_privacy_settings(user_id, privacy_settings)
    profile_manager.set_unit_preferences(user_id, unit_preferences)
    flash("Preferences updated successfully.")
    return redirect(url_for("main.profile", user_id=user_id))


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


@main.route("/group/<int:user_id>", methods=["GET", "POST"])
def group(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        flash("You need to login first", "warning")
        return redirect(url_for("main.login"))
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        group = Group(name=name, description=description)
        db.session.add(group)
        db.session.commit()
        group_member = GroupMembers(group_id=group.id, user_id=user_id)
        db.session.add(group_member)
        db.session.commit()
        return redirect(url_for("main.group", user_id=user_id))
    user_groups = Group.query.join(GroupMembers, Group.id == GroupMembers.group_id) \
                              .filter((GroupMembers.user_id == user_id)) \
                              .all()
    return render_template("group.html", groups=user_groups)


@main.route("/search", methods=["GET"])
def search_users():
    search_query = request.args.get("query", "")
    if search_query:
        results = User.query.filter(
            User.username.ilike(f"%{search_query}%")).all()
        usernames = [user.username for user in results]
        return jsonify(usernames)
    return jsonify([])

@main.route('/group/<int:group_id>/members', methods=['GET'])
def get_group_members(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    members = [
        {'id': user.id, 'username': user.username}
        for user in group.members
    ]
    return jsonify(members)