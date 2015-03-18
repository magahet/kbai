import random
from PIL import Image
import utils
import numpy as np


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
        self.answer_ids = ('1', '2', '3', '4', '5', '6')
        self.type_handlers = {
            '2x1 (Image)': self.solve2x1,
            '2x2 (Image)': self.solve2x2,
            '3x3 (Image)': self.solve3x3,
        }
        self.voters = {
            #'pixel change': self.rank_with_pixel_change,
            #'key point change': self.rank_with_key_point_change,
            'quadrant pixel change': self.rank_with_quadrant_pixel_change,
        }

    @staticmethod
    def get_figures(problem):
        figures_metadata = problem.getFigures()
        figures = {}
        for _id, figure in figures_metadata.iteritems():
            figures[_id] = Image.open(figure.getPath()).convert('1')
        return figures

    @classmethod
    def get_quadrant_pixel_count(cls, image):
        height, width = image.size
        quadrants = (
            (0, 0, width / 2, height / 2),
            (width / 2, 0, width, height / 2),
            (0, height / 2, width / 2, height),
            (width / 2, height / 2, width, height)
        )
        return np.asarray([cls.get_pixel_count(image.crop(box)) for
                           box in quadrants])

    @staticmethod
    def get_pixel_count(image, color=0):
        for count, pixel_color in image.getcolors():
            if pixel_color == color:
                return count
        return 0

    def rank_with_quadrant_pixel_change(self, problem, sample_src, sample_dst,
                                        target):
        figures = self.get_figures(problem)
        black_pixel_counts = {k: self.get_quadrant_pixel_count(i) for
                              k, i in figures.iteritems()}
        target_vector = black_pixel_counts[sample_dst] - black_pixel_counts[sample_src]
        answers = {k: utils.distance(v - black_pixel_counts[target],
                                     target_vector) for
                   k, v in black_pixel_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, 0)

    def rank_with_pixel_change(self, problem, sample_src, sample_dst, target):
        figures = self.get_figures(problem)
        black_pixel_counts = {k: i.getcolors()[0][0] for
                              k, i in figures.iteritems()}
        difference = utils.get_target_change(black_pixel_counts, sample_src,
                                             sample_dst, target)
        answers = {k: v for
                   k, v in black_pixel_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, difference)

    def rank_with_key_point_change(self, problem, sample_src, sample_dst, target):
        figures_metadata = problem.getFigures()
        key_points = {k: len(utils.get_key_points(f.getPath())) for
                      k, f in figures_metadata.iteritems()}
        difference = utils.get_target_change(key_points, sample_src,
                                             sample_dst, target)
        answers = {k: v for
                   k, v in key_points.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, difference)

    def solve2x1(self, problem):
        votes = [[k for k, _ in voter(problem, 'A', 'B', 'C')] for
                 voter in self.voters.itervalues()]
        answer = utils.first_consensus(votes)
        print problem.correctAnswer, answer
        return str(answer)

    def solve2x2(self, problem):
        votes = [[k for k, _ in voter(problem, 'A', 'B', 'C')] for
                 voter in self.voters.itervalues()]
        #votes.extend([[k for k, _ in voter(problem, 'A', 'C', 'B')] for
                      #voter in self.voters.itervalues()])
        answer = utils.first_consensus(votes)
        print problem.correctAnswer, answer
        return str(answer)

    def solve3x3(self, problem):
        return "None"

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
    def Solve(self, problem):
        problem_type = problem.getProblemType()
        if problem_type not in self.type_handlers:
            return random.choice(self.answer_ids)
        return self.type_handlers[problem_type](problem)
