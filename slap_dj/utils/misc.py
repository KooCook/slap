import warnings
from functools import wraps
from types import FunctionType
from typing import Callable


def depreciated(func: Callable = None, *, version: str = None, reason: str = None):
    """A decorator to indicate that a function or class depreciation

    Args:
        version: The version the function or class is depreciated
        reason: Optional. The reason of the depreciation.

    Returns:
        The decorator to wrap the function

    References:
        https://stackoverflow.com/questions/2536307/decorators-in-the-python-standard-lib-deprecated-specifically

    Warnings:
        Though many attributes like __name__ and __doc__ are retained,
        the __class__ of the decorated object will change to 'function'.
        Use __wrapped__ to access the wrapped object if needed.
    """
    dct = {
        FunctionType: 'function',
        type: 'class',
    }
    if func is not None:
        raise NotImplementedError("Please parameterize the decorator for now.")

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(f"{dct[type(func)].capitalize()} '{func.__name__}' is depreciated"
                          f"{f' in version {version}' if version is not None else ''}"
                          f"{f' for reason {reason}' if reason is not None else ''}", DeprecationWarning)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return decorator
