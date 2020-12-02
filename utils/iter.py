from itertools import chain, tee
from typing import Iterable, overload, TypeVar, List

__all__ = ['pairwise', 'remove_consecs']

T = TypeVar('T')


def pairwise(iterable: Iterable) -> zip:
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


@overload
def remove_consecs(lst: Iterable[T]) -> Iterable[T]: ...
@overload
def remove_consecs(lst: Iterable[T], o: T) -> Iterable[T]: ...
def remove_consecs(lst: Iterable[T], o: T = None) -> Iterable[T]:
    """Returns a list with the consecutive 'o' (if specified) removed.

    Args:
        lst: List of things
        o: Things to remove if appears consecutively.
            If None remove all consecs.
    """
    if o is None:
        raise AssertionError
    return chain((curr for curr, nxt in pairwise(lst) if not (curr == nxt == o)), lst[-1])
