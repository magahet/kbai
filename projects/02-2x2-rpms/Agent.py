from SemanticNetworkGenerator import SemanticNetworkGenerator
from FigureGenerator import FigureGenerator
from FigureMatcher import (figuresMatch, findFigureMatch)
import time
import sys
import random


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
        self.typeHandlers = {
            '2x1': self.solve2x1,
            '2x2': self.solve2x2,
        }

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
    def Solve(self, problem, timeout=10, guess=True):
        '''Solve problem and return answer choice.'''

        print '=' * 80
        print problem.name
        print problem.problemType

        return self.typeHandlers.get(problem.problemType,
                                     lambda x: '')(problem, timeout=timeout,
                                                   guess=guess)

    def solve2x1(self, problem, timeout=10, guess=True):
        # Initialize scores and current best answer.
        bestAnswer = ''
        lowestNetScore = sys.maxint
        lowestFigScore = sys.maxint
        lowestMatchScore = sys.maxint
        lowestCToAnswerScore = sys.maxint
        figureC = problem.figures.get('C')
        answerChoices = {i: problem.figures.get(i) for i in self.answerIds}
        startTime = time.time()

        # Generate and evaluate each semantic network that describes the A:B
        # relationship.
        for semanticNetwork in SemanticNetworkGenerator(problem):
            # Calculate the complexity of the transforms
            netScore = semanticNetwork.score
            print '-' * 80
            print netScore, semanticNetwork

            # Generate and evaluate each figure that can be created given
            # figure C and the semantic network.
            for figureX, figScore in FigureGenerator(figureC, semanticNetwork):
                print '.' * 80
                print 'FigureX:', figureX
                # Find the closest match between the generated figure and the
                # answer choices. Get the similarity score between the chosen
                # answer and the generated figure.
                answer, matchScore = findFigureMatch(figureX, answerChoices)

                # Could not score or there is a better matching figure
                if answer is None or matchScore > lowestMatchScore:
                    continue

                # Calculate the similarity between figure C and the chosen
                # answer.
                cToAnswerScore = figuresMatch(figureC,
                                              answerChoices.get(answer, {}))

                # Evaluate whether the current answer is better than the
                # current best answer by comparing the various scores. These
                # scores have a strict hierarchy.
                if matchScore == lowestMatchScore:
                    if netScore > lowestNetScore:
                        continue
                    if netScore == lowestNetScore:
                        if figScore > lowestFigScore:
                            continue
                        if figScore == lowestFigScore:
                            if cToAnswerScore > lowestCToAnswerScore:
                                continue
                print ('Answer: {} mScore: {} nScore: {} '
                       'fScore: {} aScore: {}').format(answer, matchScore,
                                                       netScore, figScore,
                                                       cToAnswerScore)

                # Set the current best scores
                lowestNetScore = netScore
                lowestMatchScore = matchScore
                lowestFigScore = figScore
                lowestCToAnswerScore = cToAnswerScore
                bestAnswer = answer

                # If the agent reaches the timeout limit, return the current
                # best answer.
                if time.time() > startTime + timeout:
                    return bestAnswer

        # If an answer could not be found, make a guess.
        if not bestAnswer and guess:
            bestAnswer = random.choice(self.answerIds)

        return bestAnswer

    def solve2x2(self, problem, timeout=10, guess=True):
        return ''
        # Initialize scores and current best answer.
        bestAnswer = ''
        lowestNetScore = sys.maxint
        lowestFigScore = sys.maxint
        lowestMatchScore = sys.maxint
        lowestCToAnswerScore = sys.maxint
        figureC = problem.figures.get('C')
        answerChoices = {i: problem.figures.get(i) for i in self.answerIds}
        startTime = time.time()

        # Generate and evaluate each semantic network that describes the A:B
        # relationship.
        for semanticNetwork in SemanticNetworkGenerator(problem):
            # Calculate the complexity of the transforms
            netScore = semanticNetwork.score
            print '-' * 80
            print netScore, semanticNetwork

            # Generate and evaluate each figure that can be created given
            # figure C and the semantic network.
            for figureX, figScore in FigureGenerator(figureC, semanticNetwork):
                print '.' * 80
                print 'FigureX:', figureX
                # Find the closest match between the generated figure and the
                # answer choices. Get the similarity score between the chosen
                # answer and the generated figure.
                answer, matchScore = findFigureMatch(figureX, answerChoices)

                # Could not score or there is a better matching figure
                if answer is None or matchScore > lowestMatchScore:
                    continue

                # Calculate the similarity between figure C and the chosen
                # answer.
                cToAnswerScore = figuresMatch(figureC,
                                              answerChoices.get(answer, {}))

                # Evaluate whether the current answer is better than the
                # current best answer by comparing the various scores. These
                # scores have a strict hierarchy.
                if matchScore == lowestMatchScore:
                    if netScore > lowestNetScore:
                        continue
                    if netScore == lowestNetScore:
                        if figScore > lowestFigScore:
                            continue
                        if figScore == lowestFigScore:
                            if cToAnswerScore > lowestCToAnswerScore:
                                continue
                print ('Answer: {} mScore: {} nScore: {} '
                       'fScore: {} aScore: {}').format(answer, matchScore,
                                                       netScore, figScore,
                                                       cToAnswerScore)

                # Set the current best scores
                lowestNetScore = netScore
                lowestMatchScore = matchScore
                lowestFigScore = figScore
                lowestCToAnswerScore = cToAnswerScore
                bestAnswer = answer

                # If the agent reaches the timeout limit, return the current
                # best answer.
                if time.time() > startTime + timeout:
                    return bestAnswer

        # If an answer could not be found, make a guess.
        if not bestAnswer and guess:
            bestAnswer = random.choice(self.answerIds)

        return bestAnswer
