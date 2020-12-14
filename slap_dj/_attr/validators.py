import attr
# from attr.validators import *

__all__ = ['equal_to']


@attr.s(repr=False, slots=True, hash=True)
class _EqualToValidator(object):
    expected = attr.ib()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if value != self.expected:
            raise ValueError(
                "'{name}' must be equal to expected value {expected!r}"
                " (got {value!r})".format(
                    name=attr.name, expected=self.expected, value=value
                ),
                attr,
                self.expected,
                value,
            )

    def __repr__(self):
        return f"<equal to {self.expected} validator>"


def equal_to(expected):
    """
    A validator that checks if the value is equal to expected_value.
    """
    return _EqualToValidator(expected)
