'''Provides utility functions for RPM Agent'''

import cv2
import collections
import numpy as np


def get_key_points(path):
    '''Get key points from image.
    Takes a filepath to an image'''
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    if corners is None:
        return []
    corners = np.int0(corners)
    kp = []
    for i in corners:
            kp.append(i.ravel())
    return kp


def get_target_change(obj, src, dst, target):
    return (obj[dst] * obj[target]) / obj[src]


def sorted_nn(obj, target):
    return sorted(obj.items(), key=lambda x: abs(x[1] - target))


def first_match(votes):
    closed = set([])
    while True:
        end = True
        for vote in votes:
            if not vote:
                continue
            end = False
            item = vote.pop(0)
            if item in closed:
                return item
            closed.add(item)
        if end:
            break


def first_consensus(votes):
    closed = collections.defaultdict(int)
    while True:
        end = True
        for vote in votes:
            if not vote:
                continue
            end = False
            item = vote.pop(0)
            closed[item] += 1
            if closed[item] >= len(votes) // 2:
                return item
        if end:
            break


def distance(a, b):
    return np.linalg.norm(np.asarray(a) - np.asarray(b))
