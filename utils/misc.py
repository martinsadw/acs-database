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
    a = a.astype(float)
    b = b.astype(float)
    # distance = np.dot(a, b) / np.sqrt(np.dot(a,a) * np.dot(b,b))

    numerator = np.dot(a, b)
    denominator = np.sqrt(np.dot(a,a) * np.dot(b,b))
    distance = np.divide(numerator, denominator, np.zeros_like(numerator), where=(denominator!=0))

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


def array_interleave(arr, axis=-1):
    if axis < 0:
        axis = len(arr[0].shape) + axis

    new_shape = arr[0].shape[:axis] + (arr[0].shape[axis] * len(arr),) + arr[0].shape[axis+1:]

    return np.stack(arr, axis+1).reshape(new_shape)
