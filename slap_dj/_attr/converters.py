import typing

import attr
# from attr.converters import *

__all__ = ['from_dict']

_T = typing.TypeVar('_T')
_KT = typing.TypeVar('_KT')
_VT = typing.TypeVar('_VT')


@attr.s(repr=False, slots=True, hash=True)
class _FromDictConverter:
    cls = attr.ib()

    def __call__(self, dct: typing.Dict[str, typing.Any]) -> _T:
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        return self.cls(**dct)

    def __repr__(self):
        return f"<dict to {self.cls.__name__} converter>"


def from_dict(cls: typing.Type[_T]) -> typing.Callable[[typing.Dict[str, typing.Any]], _T]:
    """
    A converter that creates an attrs instance using dct as keyword arguments.
    """
    return _FromDictConverter(cls)


@attr.s(repr=False, slots=True, hash=True)
class _IterateConverter(object):
    cls = attr.ib()

    def __call__(self, it):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        type_ = type(it)
        if type_ in (list, set):
            return type_(map(self.cls, it))
        return map(self.cls, it)

    def __repr__(self):
        return f"<iterable to {self.cls.__name__} converter>"


def iterate(cls: typing.Callable[[_KT], _VT]) -> typing.Callable[[typing.Iterable[_KT]], typing.Sequence[_VT]]:
    """
    A converter that creates an attrs instance using an iterable.
    """
    return _IterateConverter(cls)
