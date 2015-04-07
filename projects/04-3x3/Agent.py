import random
from PIL import Image
import cv2
import utils
import numpy as np


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
            #'quadrant pixel change': self.rank_with_quadrant_pixel_change,
            #'quadrant pixel change abs': self.rank_with_quadrant_pixel_change_abs,
            'quadrant pixel change and abs': self.rank_with_quadrant_pixel_change_and_abs,
            #'quadrant pixel change magnitude': self.rank_with_quadrant_pixel_change_magnitude,
            #'transformed quadrant pixel change': self.rank_with_transformed_quadrant_pixel_change,
            #'quadrant key point change': self.rank_with_quadrant_key_point_change,
        }

    @staticmethod
    def get_pil_images(problem):
        figures_metadata = problem.getFigures()
        images = {}
        for _id, figure in figures_metadata.iteritems():
            images[_id] = Image.open(figure.getPath()).convert('1')
        return images

    @staticmethod
    def get_cv2_images(problem):
        figures_metadata = problem.getFigures()
        images = {}
        for _id, figure in figures_metadata.iteritems():
            images[_id] = cv2.cvtColor(cv2.imread(figure.getPath()),
                                       cv2.COLOR_BGR2GRAY)
        return images

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

    @classmethod
    def get_segmented_pixel_count(cls, image, segment_count=1):
        segments = 4 * segment_count
        height, width = image.size
        quadrants = (
            (0, 0, width / 2, height / 2),
            (width / 2, 0, width, height / 2),
            (0, height / 2, width / 2, height),
            (width / 2, height / 2, width, height)
        )
        if segments <= 4:
            return np.asarray([cls.get_pixel_count(image.crop(box)) for
                               box in quadrants])
        else:
            return np.concatenate(
                [cls.get_segmented_pixel_count(image.crop(box), segment_count - 1) for
                 box in quadrants])

    @staticmethod
    def get_pixel_count(image, color=0):
        for count, pixel_color in image.getcolors():
            if pixel_color == color:
                return count
        return 0

    @staticmethod
    def get_key_point_count(image):
        return len(utils.get_key_points(image))

    @classmethod
    def get_quadrant_key_point_count(cls, image):
        height, width = image.shape
        quadrants = (
            (0, 0, width / 2, height / 2),
            (width / 2, 0, width, height / 2),
            (0, height / 2, width / 2, height),
            (width / 2, height / 2, width, height)
        )
        return np.asarray(
            [cls.get_key_point_count(image[box[0]:box[2], box[1]:box[3]]) for
             box in quadrants])

    def rank_with_quadrant_pixel_change_magnitude(self, problem, sample_src, sample_dst, target):
        images = self.get_pil_images(problem)
        black_pixel_counts = {k: self.get_segmented_pixel_count(i, 1) for
                              k, i in images.iteritems()}
        target_distance = utils.distance(black_pixel_counts[sample_dst],
                                         black_pixel_counts[sample_src])
        #for k, v in black_pixel_counts.iteritems():
            #if k in self.answer_ids:
                #print k, v - black_pixel_counts[target]
        answers = {k: utils.distance(v, black_pixel_counts[target]) for
                   k, v in black_pixel_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, target_distance)

    def rank_with_quadrant_pixel_change_abs(self, problem, sample_src, sample_dst, target):
        images = self.get_pil_images(problem)
        black_pixel_counts = {k: self.get_segmented_pixel_count(i, 1) for
                              k, i in images.iteritems()}
        target_vector = np.absolute(
            black_pixel_counts[sample_dst] - black_pixel_counts[sample_src])
        #print target_vector
        #for k, v in black_pixel_counts.iteritems():
            #if k in self.answer_ids:
                #print k, np.absolute(v - black_pixel_counts[target])
        answers = {k: utils.distance(
            np.absolute(v - black_pixel_counts[target]),
                   target_vector) for
                   k, v in black_pixel_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, 0)

    def rank_with_quadrant_pixel_change(self, problem, sample_src, sample_dst, target):
        images = self.get_pil_images(problem)
        black_pixel_counts = {k: self.get_segmented_pixel_count(i, 1) for
                              k, i in images.iteritems()}
        target_vector = black_pixel_counts[sample_dst] - \
            black_pixel_counts[sample_src]
        #print target_vector
        #for k, v in black_pixel_counts.iteritems():
            #if k in self.answer_ids:
                #print k, v - black_pixel_counts[target]
        answers = {k: utils.distance(v - black_pixel_counts[target],
                                     target_vector) for
                   k, v in black_pixel_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, 0)

    def rank_with_quadrant_pixel_change_and_abs(self, problem, sample_src, sample_dst, target):
        images = self.get_pil_images(problem)
        black_pixel_counts = {k: self.get_segmented_pixel_count(i, 1) for
                              k, i in images.iteritems()}
        target_vector = (black_pixel_counts[sample_dst] -
                         black_pixel_counts[sample_src])
        abs_target_vector = np.absolute(target_vector)
        #print 't', target_vector
        answers = []
        for label, pixel_counts in black_pixel_counts.iteritems():
            if label not in self.answer_ids:
                continue
            diff_vector = pixel_counts - black_pixel_counts[target]
            distance = utils.distance(diff_vector, target_vector)
            answers.append((label, distance))

            abs_diff_vector = np.absolute(diff_vector)
            abs_distance = utils.distance(abs_diff_vector, abs_target_vector)
            answers.append((label, abs_distance))

            #print label, diff_vector, distance, abs_distance

        return utils.sorted_nn(answers, 0)

    def rank_with_pixel_change(self, problem, sample_src, sample_dst, target):
        images = self.get_pil_images(problem)
        black_pixel_counts = {k: self.get_pixel_count(i) for
                              k, i in images.iteritems()}
        difference = utils.get_target_change(black_pixel_counts, sample_src,
                                             sample_dst, target)
        answers = {k: v for
                   k, v in black_pixel_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, difference)

    def rank_with_quadrant_key_point_change(
        self, problem, sample_src, sample_dst,
            target):
        images = self.get_cv2_images(problem)
        key_point_counts = {k: self.get_quadrant_key_point_count(i) for
                            k, i in images.iteritems()}
        target_vector = key_point_counts[sample_dst] - \
            key_point_counts[sample_src]
        answers = {k: utils.distance(v - key_point_counts[target],
                                     target_vector) for
                   k, v in key_point_counts.iteritems() if
                   k in self.answer_ids}
        return utils.sorted_nn(answers, 0)

    def rank_with_key_point_change(self, problem, sample_src, sample_dst, target):
        images = self.get_cv2_images(problem)
        key_points = {k: self.get_key_point_count(i) for
                      k, i in images.iteritems()}
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
        #print problem.correctAnswer, answer
        return str(answer)

    def solve2x2(self, problem):
        votes = [[k for k, _ in voter(problem, 'A', 'B', 'C')] for
                 voter in self.voters.itervalues()]
        #votes.extend([[k for k, _ in voter(problem, 'A', 'C', 'B')] for
                      #voter in self.voters.itervalues()])
        answer = utils.first_consensus(votes)
        #print problem.correctAnswer, answer
        return str(answer)

    def solve3x3(self, problem):
        votes = [[k for k, _ in voter(problem, 'A', 'E', 'E')] for
                 voter in self.voters.itervalues()]
        votes.extend([[k for k, _ in voter(problem, 'A', 'C', 'G')] for
                      voter in self.voters.itervalues()])
        votes.extend([[k for k, _ in voter(problem, 'B', 'C', 'H')] for
                      voter in self.voters.itervalues()])
        votes.extend([[k for k, _ in voter(problem, 'E', 'F', 'H')] for
                      voter in self.voters.itervalues()])
        answer = utils.first_consensus(votes)
        #print problem.correctAnswer, answer
        return str(answer)

    def Solve(self, problem):
        print problem.getName()
        problem_type = problem.getProblemType()
        if problem_type not in self.type_handlers:
            return random.choice(self.answer_ids)
        return self.type_handlers[problem_type](problem)
