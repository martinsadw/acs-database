import numpy as np


def hamming_distance(a, b, axis=None, normalize=True):
    if axis is None:
        distance = np.sum(a != b)
    else:
        distance = np.sum(a != b, axis=axis)

    if normalize:
        distance = distance * (distance.size / a.size)

    return distance


def cosine_similarity(a, b):
    a = a.astype(int)
    b = b.astype(int)
    distance = np.dot(a, b) / np.sqrt(np.dot(a,a) * np.dot(b,b))

    return distance


def cosine_distance(a, b):
    return 1 - cosine_similarity(a, b)


def grade_distance(a, b, axis=None):
    if axis is None:
        distance = np.sum(np.abs(a - b))
    else:
        distance = np.sum(np.abs(a - b), axis=axis)

    return distance


def style_distance(a, b, axis=None):
    if axis is None:
        distance = np.sum(np.abs(a - b))
    else:
        distance = np.sum(np.abs(a - b), axis=axis)

    return distance
