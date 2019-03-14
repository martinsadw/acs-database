import numpy as np


def save_csv(name, values):
    np.savetxt(name, values, fmt="%7.3f", delimiter=",")
