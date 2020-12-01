import numpy as np
from scipy import integrate
from scipy import special


def logistic(x):
    return special.expit(x)


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
    f = logistic
    print(f.__name__)
    for i in range(1, 11):
        print(i, f(i))
