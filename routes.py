from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, WorkoutLog, Group, Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Perform login
            return redirect(url_for('main.profile', user_id=user.id))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@main.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@main.route('/workout_log', methods=['GET', 'POST'])
def workout_log():
    if request.method == 'POST':
        user_id = request.form['user_id']
        exercises = request.form['exercises']
        notes = request.form['notes']
        workout_log = WorkoutLog(user_id=user_id, exercises=exercises, notes=notes)
        db.session.add(workout_log)
        db.session.commit()
        return redirect(url_for('main.profile', user_id=user_id))
    return render_template('workout_log.html')

@main.route('/group', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        group = Group(name=name, description=description)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('main.group'))
    groups = Group.query.all()
    return render_template('group.html', groups=groups)