from itertools import chain, tee, zip_longest
from typing import Any, Iterable, Tuple, TypeVar, Union, overload

__all__ = ['pairwise', 'remove_consecs']

T = TypeVar('T')


@overload
def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]: ...
@overload
def pairwise(iterable: Iterable[T], fillvalue: Any) -> Iterable[Tuple[T, T]]: ...
def pairwise(iterable: Iterable[T], fillvalue: Any = None) -> Iterable[Tuple[T, Union[T, Any]]]:
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
    return chain((curr for curr, nxt in pairwise(lst, None) if not (curr == nxt == o)))
