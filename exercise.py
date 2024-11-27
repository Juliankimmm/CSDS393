class Exercise:
    def __init__(self, exerciseID):
        self.exerciseID = exerciseID
        self.exerciseName = ""
        self.exerciseSets = 0
        self.exerciseWeights = []
        self.exerciseRPEs = []


# 5.6.1 GetExerciseName
def GetExerciseName(self):
    return self.exerciseName


# 5.6.2 SetExerciseName
def SetExerciseName(self, exerciseName):
    self.exerciseName = exerciseName


# 5.6.3 GetExerciseSets
def GetExerciseSets(self):
    return self.exerciseSets


# 5.6.4 SetExerciseSets
def SetExerciseSets(self, exerciseSets):
    self.exerciseSets = exerciseSets


# 5.6.5 GetExerciseWeights
def GetExerciseWeights(self):
    return self.exerciseWeights


# 5.6.6 SetExerciseWeights
def SetExerciseWeights(self, exerciseWeights):
    if len(exerciseWeights) == self.exerciseSets:
        self.exerciseWeights = exerciseWeights


# 5.6.7 GetExerciseRPEs
def GetExerciseRPEs(self):
    return self.exerciseRPEs


# 5.6.8 SetExerciseRPEs
def SetExerciseRPEs(self, exerciseRPEs):
    if len(exerciseRPEs) == self.exerciseSets:
        self.exerciseRPEs = exerciseRPEs
