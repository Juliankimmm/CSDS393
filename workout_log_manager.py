from models import db, User
class WorkoutLogManager:
    def __init__(self):
        self.logs = []
        self.users = {}

    def PostLog(self, logID, userID):
        # Updates log and post history for the user
        user = self.users.get(userID)
        if user:
            user['post_history'].append(logID)
            # Add log to friends' feeds
            for friend in user['friends']:
                friend['feed'].append(logID)

    def CreateWorkoutLog(self):
        # Generate a new log ID
        logID = len(self.logs) + 1
        new_log = WorkoutLog(logID)
        self.logs.append(new_log)
        return logID

    def EditWorkoutLog(self, logID):
        log = next((log for log in self.logs if log.logID == logID), None)
        if log:
            log.editing = True

    def DeleteWorkoutLog(self, logID):
        self.logs = [log for log in self.logs if log.logID != logID]
        for user in self.users.values():
            user['post_history'] = [log for log in user['post_history'] if log != logID]

    def CompleteWorkoutLog(self, logID):
        log = next((log for log in self.logs if log.logID == logID), None)
        if log:
            log.complete = True
            user = self.users.get(log.userID)
            if user:
                user['workout_history'].append(logID)

class WorkoutLog:
    def __init__(self, logID):
        self.logID = logID
        self.exercises = []
        self.name = ""
        self.notes = ""
        self.userID = None
        self.complete = False
        self.editing = False

    def AddExercise(self, exerciseID):
        self.exercises.append(exerciseID)

    def RemoveExercise(self, exerciseID):
        self.exercises = [ex for ex in self.exercises if ex != exerciseID]

    def EditExercise(self, exerciseID):
        # Find exercise and edit it
        pass

    def GetLogName(self):
        return self.name

    def SetLogName(self, logName):
        self.name = logName

    def GetLogNotes(self):
        return self.notes

    def SetLogNotes(self, logNotes):
        self.notes = logNotes

    def AddSet(self, exerciseID):
        # Add set to the specific exercise
        pass

    def RemoveSet(self, exerciseID):
        # Remove set from the specific exercise
        pass

    def UpdateWeight(self, exerciseID, exerciseWeight):
        # Update weight used for the exercise
        pass

    def UpdateRPE(self, exerciseID, exerciseRPE):
        # Update RPE value for the exercise
        pass