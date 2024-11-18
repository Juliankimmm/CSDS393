from models import db, WorkoutLog, User, Exercise
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class WorkoutLogManager:
    def __init__(self):
        self.logs = []
        self.users = {}

    def PostLog(self, logID, userID):
        # Updates log and post history for the user
        user = User.query.get(userID)
        if user:
            log = WorkoutLog.query.get(logID)
            if log:
                user.post_history.append(logID)
                # Add log to friends' feeds
                for friend in user.friends:
                    friend.feed.append(logID)
                db.session.commit()

    def CreateWorkoutLog(self, userID):
        # Generate a new log and add to database
        new_log = WorkoutLog(user_id=userID)  # Assuming userID is passed and linked to the log
        db.session.add(new_log)
        db.session.commit()
        return new_log.id

    def EditWorkoutLog(self, logID, new_name=None, new_notes=None):
        log = WorkoutLog.query.get(logID)
        if log:
            if new_name:
                log.name = new_name
            if new_notes:
                log.notes = new_notes
            log.editing = True
            db.session.commit()

    def DeleteWorkoutLog(self, logID):
        log = WorkoutLog.query.get(logID)
        if log:
            db.session.delete(log)
            db.session.commit()

        # Remove log from users' post history
        users = User.query.all()
        for user in users:
            user.post_history = [log_id for log_id in user.post_history if log_id != logID]
        db.session.commit()

    def CompleteWorkoutLog(self, logID):
        log = WorkoutLog.query.get(logID)
        if log:
            log.complete = True
            db.session.commit()
            user = User.query.get(log.user_id)
            if user:
                user.workout_history.append(logID)
            db.session.commit()

class WorkoutLog(db.Model):
    __tablename__ = 'workout_log'

    logID = db.Column(db.Integer, primary_key=True)  # logID as primary key
    name = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))  # Assuming you have a user model
    complete = db.Column(db.Boolean, default=False)
    editing = db.Column(db.Boolean, default=False)

    # Define a relationship to Exercise, assuming you have an Exercise model
    exercises = db.relationship('Exercise', secondary='workout_log_exercise', backref='workout_logs')

    def __init__(self, name, notes, userID):
        self.name = name
        self.notes = notes
        self.userID = userID

    # Add exercise to the workout log
    def add_exercise(self, exerciseID):
        exercise = Exercise.query.get(exerciseID)  # Fetch the Exercise from the database
        if exercise:
            self.exercises.append(exercise)
            db.session.commit()

    # Remove exercise from the workout log
    def remove_exercise(self, exerciseID):
        exercise = Exercise.query.get(exerciseID)
        if exercise in self.exercises:
            self.exercises.remove(exercise)
            db.session.commit()

    # Edit an exercise's details (this would depend on what exactly you want to edit)
    def edit_exercise(self, exerciseID, new_details):
        exercise = Exercise.query.get(exerciseID)
        if exercise:
            exercise.details = new_details  # Modify details as needed
            db.session.commit()

    def get_log_name(self):
        return self.name

    def set_log_name(self, logName):
        self.name = logName
        db.session.commit()

    def get_log_notes(self):
        return self.notes

    def set_log_notes(self, logNotes):
        self.notes = logNotes
        db.session.commit()
        '''
    # Add set to the exercise (assuming you have a 'Set' model)
    def add_set(self, exerciseID, set_details):
        exercise = Exercise.query.get(exerciseID)
        if exercise:
            new_set = Set(exercise_id=exercise.id, **set_details)
            db.session.add(new_set)
            db.session.commit()

    # Remove set from exercise
    def remove_set(self, exerciseID, setID):
        set_to_remove = Set.query.get(setID)
        if set_to_remove and set_to_remove.exercise_id == exerciseID:
            db.session.delete(set_to_remove)
            db.session.commit()
        '''
    # Update weight used for the exercise
    def update_weight(self, exerciseID, exerciseWeight):
        exercise = Exercise.query.get(exerciseID)
        if exercise:
            exercise.weight = exerciseWeight
            db.session.commit()

    # Update RPE value for the exercise
    def update_rpe(self, exerciseID, exerciseRPE):
        exercise = Exercise.query.get(exerciseID)
        if exercise:
            exercise.rpe = exerciseRPE
            db.session.commit()