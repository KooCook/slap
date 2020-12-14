from itertools import chain, tee, zip_longest
from typing import Iterable, Tuple, TypeVar, Union

__all__ = ['pairwise', 'remove_consecs']

_T = TypeVar('_T')
_S = TypeVar('_S')


def pairwise(iterable: Iterable[_T], fillvalue: _S = None) -> Iterable[Tuple[_T, Union[_T, _S]]]:
    """
    Returns the iterable pairwise.
    If `fillvalue` is not provided, does not return last value.

    Args:
        iterable: The iterable to make pairwise
        fillvalue: The value to fill for the last value. Passed to zip_longest.

    Examples:
        s[0:10] -> (s0,s1), (s1,s2), (s2, s3), ..., (s8, s9)
        s[0:10], None -> (s0,s1), (s1,s2), (s2, s3), ..., (s8, s9), (s9, None)
    """
    a, b = tee(iterable)
    next(b, None)
    if fillvalue is not None:
        return zip_longest(a, b, fillvalue=fillvalue)
    return zip(a, b)


def remove_consecs(lst: Iterable[_T], o: _T = None) -> Iterable[_T]:
    """Returns a list with the consecutive 'o' (if specified) removed.

    Args:
        lst: List of things
        o: Things to remove if appears consecutively.
            If None remove all consecs.
    """
    if o is None:
        raise AssertionError
    return chain((curr for curr, nxt in pairwise(lst, None) if not (curr == nxt == o)))
