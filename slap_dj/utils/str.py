import string

from utils.iter import remove_consecs

__all__ = ['snake_to_camel', 'camel_to_snake', 'to_all_caps', 'snake_to_capwords', 'snake_case', 'camel_to_capwords']


def snake_case(s: str) -> str:
    """Convert string into snake case.
    Join punctuation (-, space, .) with underscore

    Args:
        string: String to convert.

    Returns:
        string: Snake cased string.
    """
    lst = []
    for c in s:
        if c in '-.' + string.whitespace:
            lst.append('_')
        elif c in string.ascii_uppercase:
            lst.extend(['_', c.lower()])
        else:
            lst.append(c)
    return ''.join(remove_consecs(lst, '_'))


def snake_to_camel(s: str) -> str:
    """Returns a new str in camelCase, given an str in snake_case.
    Removes all underscore before and after.

    Examples:
        >>> snake_to_camel('snake_to_camel')
        'snakeToCamel'
        >>> snake_to_camel('__snake_to_camel__')
        'snakeToCamel'
        >>> snake_to_camel('alreadyCamel')
        'alreadyCamel'
        >>> snake_to_camel('lonesnake')
        'lonesnake'
    """
    try:
        first, *others = [word for word in s.split('_') if word]
        return first + ''.join(s.title() for s in others)
    except ValueError:
        return s


def snake_to_capwords(s: str) -> str:
    """Returns a new str in CapWords, given an str in snake_case.
    Removes all underscore before and after.

    Examples:
        >>> snake_to_capwords('snake_to_capwords')
        'SnakeToCapwords'
        >>> snake_to_capwords('__snake_to_capwords__')
        'SnakeToCapwords'
        >>> snake_to_capwords('camelCase')
        Traceback (most recent call last):
          ...
        ValueError: original str is not in snake_case: 'camelCase'
        >>> snake_to_capwords('lonesnake')
        'Lonesnake'
        >>> snake_to_capwords('title_akas')
        'TitleAkas'
    """
    words = [word for word in s.split('_') if word]
    if len(words) == 1:
        for char in words[0]:
            if char.isupper():
                raise ValueError(f"original str is not in snake_case: '{s}'")
        return s.title()
    return ''.join(s.title() for s in words)


def camel_to_snake(s: str) -> str:
    """Returns a new str in snake_case, given an str in camelCase.

    Raises:
        ValueError: When original str is not in camelCase

    Examples:
        >>> camel_to_snake('camelToSnake')
        'camel_to_snake'
        >>> camel_to_snake('already_snake')
        Traceback (most recent call last):
          ...
        ValueError: original str is not in camelCase: 'already_snake'
        >>> camel_to_snake('lonecamel')
        'lonecamel'
        >>> camel_to_snake('CapWords')
        'cap_words'
        >>> camel_to_snake('Ugly_Case')
        Traceback (most recent call last):
          ...
        ValueError: original str is not in camelCase: 'Ugly_Case'
    """
    if '_' in s:
        raise ValueError("original str is not in camelCase: '{}'".format(s))
    for u in string.ascii_uppercase:
        s = s.replace(u, '_' + u.lower())
    if s.startswith('_'):
        # _cap_words
        return s[1:]
    return s


def to_all_caps(s: str) -> str:
    """Returns a new str in CONSTANT_CASE, given any str.

    Examples:
        >>> to_all_caps('to_constant')
        'TO_CONSTANT'
        >>> to_all_caps('Meals, Entrees, and Side Dishes')
        'MEALS_ENTREES_AND_SIDE_DISHES'
        >>> to_all_caps('American Indian/Alaska Native Foods')
        'AMERICAN_INDIANALASKA_NATIVE_FOODS'
    """
    s = s.replace(' ', '_')
    s = ''.join(c.upper() for c in s if c in string.ascii_letters or c in '_')
    assert s.isidentifier(), s
    return s


def trim_spaces(s: str) -> str:
    """Trims excess spaces

    Examples:
        >>> trim_spaces(' pretty')
        'pretty'
        >>> trim_spaces(' CHEDDAR CHEESE')
        'CHEDDAR CHEESE'
        >>> trim_spaces(' salt  ')
        'salt'
    """
    return ' '.join(_ for _ in s.split(' ') if _)


def camel_to_capwords(s: str, validate: bool = False) -> str:
    """Coverts camelCase to CapWords

    Examples:
        >>> camel_to_capwords('camelCase')
        'CamelCase'
        >>> camel_to_capwords('salt')
        'Salt'
        >>> camel_to_capwords('')
        ''
    """
    if validate:
        raise NotImplementedError
    try:
        # return s[0].upper() + s[1:]
        it = iter(s)
        return next(it).upper() + ''.join(it)
    except IndexError:
        # from accessing s[0]
        pass
    except StopIteration:
        # from joining empty iterable
        pass
    return ''


if __name__ == '__main__':
    import doctest

    doctest.testmod()
