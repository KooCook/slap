from typing import Iterable, Tuple, TypeVar, Union, overload

_T = TypeVar('_T')
_S = TypeVar('_S')

@overload
def pairwise(iterable: Iterable[_T]) -> Iterable[Tuple[_T, _T]]: ...
@overload
def pairwise(iterable: Iterable[_T], fillvalue: _S) -> Iterable[Tuple[_T, Union[_T, _S]]]: ...

@overload
def remove_consecs(lst: Iterable[_T]) -> Iterable[_T]: ...
@overload
def remove_consecs(lst: Iterable[_T], o: _T) -> Iterable[_T]: ...
