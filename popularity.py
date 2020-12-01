import numpy as np
from scipy import integrate
from scipy import special
from functools import partial


def logistic(x):
    return special.expit(x)


def logistic2(L, k, x0, x):
    """

    Args:
        L: the curve's maximum value
        k: the logistic growth rate or steepness of the curve
        x0: the x value of the sigmoid's midpoint
        x: the input
    """
    return np.divide(L, np.add(1, np.exp(np.negative(np.multiply(k, np.subtract(x, x0))))))


def tanh(x):
    return np.tanh(x)


def arctan(x):
    return np.arctan(x)


def _f(t):
    return np.exp(-np.power(t, 2))


def erf(x):
    return special.erf(x)


def func1(x):
    return np.divide(x, np.abs(x) + 1)


if __name__ == '__main__':
    for f in [
        logistic,
        partial(logistic2, 1, 1, 0),
        # tanh,
        # arctan,
        # erf,
        # func1,
    ]:
        try:
            print(f.__name__)
        except AttributeError:
            print(f.func.__name__)
        for i in range(1, 16):
            print(i, f(i))
        print()
