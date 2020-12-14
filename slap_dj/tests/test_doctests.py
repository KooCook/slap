import unittest
from doctest import DocTestSuite

from utils import nlp


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore) -> unittest.TestSuite:
    modules_to_test = (nlp,)
    tests.addTests(map(DocTestSuite, modules_to_test))
    return tests


if __name__ == '__main__':
    unittest.main()
