import random
from PIL import Image
import numpy as np
import utils


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
            '2x2 (Image)': self.solve2x1,
            '3x3 (Image)': self.solve3x3,
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
    def Solve(self, problem):
        problem_type = problem.getProblemType()
        if problem_type not in self.type_handlers:
            return random.choice(self.answer_ids)
        return self.type_handlers[problem_type](problem)

    def solve2x1(self, problem):
        figures_metadata = problem.getFigures()
        figures = {}
        for _id, figure in figures_metadata.iteritems():
            image = Image.open(figure.getPath()).convert('1')
            figures[_id] = np.asarray(image.getdata())
        white_pixel_counts = {k: np.count_nonzero(a) for
                              k, a in figures.iteritems()}
        kps = {k: len(utils.get_key_points(f.getPath())) for
               k, f in figures_metadata.iteritems()}
        target = ((white_pixel_counts['B'] * white_pixel_counts['C']) /
                  white_pixel_counts['A'])
        target_kp = (kps['B'] * kps['C']) / kps['A']
        white_pixel_counts_answers = {k: v for
                                      k, v in white_pixel_counts.iteritems() if
                                      k in self.answer_ids}
        kp_answers = {k: v for
                      k, v in kps.iteritems() if
                      k in self.answer_ids}
        pc = sorted_nn(white_pixel_counts_answers, target)
        kp = sorted_nn(kp_answers, target_kp)
        answer = first_match([k for k, _ in pc], [k for k, _ in kp])
        print problem.correctAnswer, answer
        return str(answer)

    def solve2x2(self, problem):
        return "None"

    def solve3x3(self, problem):
        return "None"


def sorted_nn(obj, target):
    return sorted(obj.items(), key=lambda x: abs(x[1] - target))


def first_match(list1, list2):
    closed = set([])
    while list1 and list2:
        if list1:
            item = list1.pop(0)
            if item in closed:
                return item
            closed.add(item)
        if list2:
            item = list2.pop(0)
            if item in closed:
                return item
            closed.add(item)
