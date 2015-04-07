'''Provides utility functions for RPM Agent'''

import cv2
import collections
import numpy as np


def get_key_points(image):
    '''Get key points from image.'''
    corners = cv2.goodFeaturesToTrack(image, 25, 0.01, 10)
    if corners is None:
        return []
    corners = np.int0(corners)
    kp = []
    for i in corners:
            kp.append(i.ravel())
    return kp


def get_target_change(obj, src, dst, target):
    if obj[src] == 0:
        obj[src] = 1
    return (obj[dst] * obj[target]) / obj[src]


def sorted_nn(obj, target):
    if isinstance(obj, dict):
        obj = obj.items()
    return sorted(obj, key=lambda x: abs(x[1] - target))


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
    return np.linalg.norm(np.asarray(a) - np.asarray(b)).astype(int)


def get_similarity(a, b):
    im1 = np.asarray(a).astype(np.bool)
    im2 = np.asarray(b).astype(np.bool)
    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")
    intersection = np.logical_and(im1, im2)
    union = np.logical_or(im1, im2)
    return intersection.sum() / float(union.sum())
