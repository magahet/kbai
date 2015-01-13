# DO NOT MODIFY THIS FILE.
#
# When you submit your project, an alternate version of this file will be used
# to test your code against the sample Raven's problems in this zip file, as
# well as other problems from the Raven's Test and former students.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.
#
#

import os
from Agent import Agent
from ProblemSet import ProblemSet

# The main driver file for Project1. You may edit this file to change which
# problems your Agent addresses while debugging and designing, but you should
# not depend on changes to this file for final execution of your project. Your
# project will be graded using our own version of this file.
sets=[] # The variable 'sets' stores multiple problem sets.
        # Each problem set comes from a different folder in /Problems/
        # Additional sets of problems will be used when grading projects.
        # You may also write your own problems.

for file in os.listdir("Problems"): # One problem set per folder in /Problems/
    newSet = ProblemSet(file)       # Each problem set is named after the folder in /Problems/
    sets.append(newSet)
    for problem in os.listdir("Problems" + os.sep + file):  # Each file in the problem set folder becomes a problem in that set.
        f = open("Problems" + os.sep + file + os.sep + problem) # Make sure to add only problem files to subfolders of /Problems/
        newSet.addProblem(f)

# Initializing problem-solving agent from Agent.java
agent=Agent()   # Your agent will be initialized with its default constructor.
                # You may modify the default constructor in Agent.java
