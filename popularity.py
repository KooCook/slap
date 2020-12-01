import numpy as np
from scipy import integrate


def logistic(x):
    return np.divide(1, np.add(1, np.exp(np.negative(x))))


def tanh(x):
    return np.tanh(x)


def arctan(x):
    return np.arctan(x)


def _f(t):
    return np.exp(-np.power(t, 2))


def erf(x):
    return np.divide(2, np.sqrt(np.pi)) * integrate.quad(_f, 0, x)[0]


def func1(x):
    return np.divide(x, np.abs(x) + 1)


if __name__ == '__main__':
    f = logistic
    print(f.__name__)
    for i in range(1, 11):
        print(i, f(i))
