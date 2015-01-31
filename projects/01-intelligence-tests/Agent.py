from SemanticNetwork import (SemanticNetworkGenerator, FigureGenerator)
from Utils import findFigureMatch
import time
import sys


# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.answerIds = ['1', '2', '3', '4', '5', '6']

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self, problem, timeout=10):
        print problem.name
        bestAnswer = ''
        lowestNetScore = sys.maxint
        lowestFigScore = sys.maxint
        lowestMatchScore = sys.maxint
        figureC = problem.figures.get('C')
        answerChoices = {i: problem.figures.get(i) for i in self.answerIds}
        startTime = time.time()
        for semanticNetwork in SemanticNetworkGenerator(problem):
            netScore = semanticNetwork.score
            # DEBUG
            #if netScore != 3:
                #continue
            if time.time() > startTime + timeout:
                return bestAnswer
            print netScore, semanticNetwork
            for figureX, figScore in FigureGenerator(figureC, semanticNetwork):
                #if len(semanticNetwork.transforms) > 0 and figuresMatch(figureX, figureC, simpleMatch=True):
                    #continue
                if time.time() > startTime + timeout:
                    return bestAnswer
                print figureX
                answer, matchScore = findFigureMatch(figureX, answerChoices)
                if answer is None or matchScore > lowestMatchScore:
                    continue
                if matchScore == lowestMatchScore and netScore > lowestNetScore:
                    continue
                if netScore == lowestNetScore and figScore > lowestFigScore:
                    continue
                print 'match:', answer, matchScore
                lowestNetScore = netScore
                lowestMatchScore = matchScore
                bestAnswer = answer
                #if lowestMatchScore == 0:
                    #break

        return bestAnswer
