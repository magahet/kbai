import random
from PIL import (Image, ImageOps)
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
            'affine': self.rank_with_affine,
        }
        self.transforms = {
            'no change': lambda i: i,
            'mirror': lambda i: ImageOps.mirror(i),
            'flip': lambda i: ImageOps.flip(i),
            'rotate 90': lambda i: i.rotate(90),
            'rotate 180': lambda i: i.rotate(180),
            'rotate 270': lambda i: i.rotate(270),
        }

    @staticmethod
    def get_pil_images(problem):
        figures_metadata = problem.getFigures()
        images = {}
        for _id, figure in figures_metadata.iteritems():
            images[_id] = Image.open(figure.getPath())
        return images

    def rank_with_affine(self, problem, sample_src, sample_dst, target):
        images = self.get_pil_images(problem)
        max_similarity = 0.0
        for name, func in self.transforms.iteritems():
            similarity = utils.get_similarity(func(images[sample_src]), images[sample_dst])
            #print name, similarity
            if similarity > max_similarity:
                max_similarity = similarity
                best, transform = name, func
        #print best, max_similarity
        transformed_image = transform(images[target])
        transformed_image.save('/tmp/test.png')
        answers = {}
        #print np.asarray(transformed_image)
        for name, image in images.iteritems():
            if name not in self.answer_ids:
                continue
            #print name, utils.get_similarity(transformed_image, image)
            image.save('/tmp/{}.png'.format(name))
            answers[name] = utils.get_similarity(transformed_image, image)
        return answers

    def solve2x1(self, problem):
        rank = self.rank_with_affine(problem, 'A', 'B', 'C')
        return max(rank, key=lambda i: rank[i])

    def solve2x2(self, problem):
        rank = self.rank_with_affine(problem, 'A', 'B', 'C')
        #rank_horrizontal = self.rank_with_affine(problem, 'A', 'B', 'C')
        #rank_vertical = self.rank_with_affine(problem, 'A', 'C', 'B')
        #rank = {k: np.average([rank_horrizontal[k], rank_vertical[k]]) for
                #k in self.answer_ids}
        return max(rank, key=lambda i: rank[i])

    def solve3x3(self, problem):
        return "None"

    def Solve(self, problem):
        print problem.getName()
        problem_type = problem.getProblemType()
        if problem_type not in self.type_handlers:
            return random.choice(self.answer_ids)
        return self.type_handlers[problem_type](problem)
