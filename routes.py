from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, WorkoutLog, Group, Post
from user_profile_manager import UserProfileManager

main = Blueprint('main', __name__)
profile_manager = UserProfileManager()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/update_preferences/<int:user_id>', methods=['POST'])
def update_preferences(user_id):
    # Fetch privacy and unit preferences from the form
    privacy_settings = request.form.get('privacy_settings')
    unit_preferences = request.form.get('unit_preferences')
    
    # Update preferences via UserProfileManager
    profile_manager.set_privacy_settings(user_id, privacy_settings)
    profile_manager.set_unit_preferences(user_id, unit_preferences)
    
    # Show success message and redirect to profile page
    flash("Preferences updated successfully.")
    return redirect(url_for('main.profile', user_id=user_id))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Perform login
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.profile', user_id=user.id))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@main.route('/create_account', methods=['POST'])
def create_account():
    username = request.form['new-username']
    password = request.form['new-password']
    bio = request.form.get('bio', '')
    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists', 'danger')
        return redirect(url_for('main.create_account'))  
    # Call create_user_profile method from user_profile_manager
    new_user = profile_manager.create_user_profile(username, password, bio)
    # Log the user in by adding their ID to the session
    session['user_id'] = new_user.id
    flash('Account created successfully!', 'success')
    return redirect(url_for('main.profile', user_id=new_user.id))

@main.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('You need to log in first', 'warning')
        return redirect(url_for('main.login'))
    user = User.query.get_or_404(user_id)
    workout_logs = WorkoutLog.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', user=user, workout_logs=workout_logs)

@main.route('/workout_log/<int:user_id>', methods=['GET', 'POST'])
def workout_log(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('You need to login first', 'warning')
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        user_id = session['user_id']
        exercise = request.form['exercise']
        reps = request.form['reps']
        weight = request.form['weight']
        rpe = request.form['rpe']

        # Create a new instance of WorkoutLog
        workout_log = WorkoutLog(user_id=user_id)
        workout_log.exercise = exercise
        workout_log.reps = reps
        workout_log.weight = weight
        workout_log.rpe = rpe

        # Add the new workout log entry to the session and commit
        db.session.add(workout_log)
        db.session.commit()

        return redirect('/workout_log')  # Redirect to show the updated log

    return render_template('workout_log.html')

@main.route('/group/<int:user_id>', methods=['GET', 'POST'])
def group(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('You need to login first', 'warning')
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        group = Group(name=name, description=description)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('main.group'))
    groups = Group.query.all()
    return render_template('group.html', groups=groups)

if __name__ == "__main__":
    app.run(debug=True)