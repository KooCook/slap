import typing

import yaml

import attr

from utils.str import camel_to_capwords

path_to_converters = '_attr.c'
path_to_validators = '_attr.v'

template = """
{
  "kind": "youtube#videoListResponse",
  "etag": etag,
  "nextPageToken": string,
  "prevPageToken": string,
  "pageInfo": {
    "totalResults": integer,
    "resultsPerPage": integer
  },
  "items": [
    video Resource
  ]
}
""".strip()


def write_attrib(attrib: str, cls: typing.Union[type, str], convert: bool = None, validate: bool = True, equal_to: typing.Any = None, optional: bool = False):
    if convert is None:
        convert = cls in (str, int, float)

    kwargs = []

    if optional:
        kwargs.append("default=None")

    if isinstance(cls, type):
        clsname = cls.__name__
        if convert:
            if attr.has(cls):
                kwargs.append(f"converter={path_to_converters}.from_dict({clsname})")
            elif cls == list:
                kwargs.append(f"converter=list")
            elif cls == dict:
                kwargs.append(f"converter=dict")
    elif isinstance(cls, str):
        clsname = cls
        if convert:
            if clsname in ('str', 'int', 'float'):
                kwargs.append(f"converter={path_to_converters}.from_dict({clsname})")
    elif isinstance(cls, type(typing.List)):
        if cls._name == 'List':
            item = cls.__args__[0]
            if isinstance(item, typing.ForwardRef):
                item_name = item.__forward_arg__
            elif isinstance(item, type):
                item_name = item.__name__
            else:
                raise cls
            clsname = f'List[{item_name}]'
            kwargs.append(f"converter={path_to_converters}.iterate({path_to_converters}.from_dict({item_name}))")
        else:
            raise cls
    else:
        raise TypeError(f"'cls' must be a 'type' or a 'str', not {cls!r}")

    if validate:
        if optional:
            _base = 'validator=attr.validators.optional([{val}])'
        else:
            _base = 'validator=[{val}]'
        val = []
        if isinstance(cls, type(typing.List)):
            val.append(
            f"attr.validators.deep_iterable(member_validator=attr.validators.instance_of({item_name}), iterable_validator=attr.validators.instance_of({cls.__origin__.__name__}))")
        else:
            val.append(f'attr.validators.instance_of({clsname})')
        if equal_to is not None:
            val.append(f'{path_to_validators}.equal_to({repr(equal_to)})')
        kwargs.append(_base.format(val=', '.join(val)))
    return f"    {attrib}: {clsname} = attr.ib({', '.join(kwargs)})"


def main():
    tmp = yaml.load(template, Loader=yaml.FullLoader)
    print(tmp)

    lines = [
        f'@attr.s',
        f'class {camel_to_capwords(tmp["kind"].split("#")[1])}',
    ]
    for k, v in tmp.items():
        if isinstance(v, str):
            try:
                t = {
                    'string': str,
                    'integer': int,
                    'decimal': float,
                }
            except KeyError:
                pass # DO STH
        
        write_attrib(k, )
        f'     kind: str = attr.ib(validator=[attr.validators.instance_of(str), attr.v.equal_to("youtube#videoListResponse")])',
        f'     etag: str = attr.ib(validator=[attr.validators.instance_of(str)])',
        f'     pageInfo: PageInfo = attr.ib(converter=attr.c.from_dict(PageInfo), validator=[attr.validators.instance_of(PageInfo)])',
        f'     items: List[VideoResource] = attr.ib()',
        f'     nextPageToken: str = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))',
        f'     prevPageToken: str = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))',
    ]

if __name__ == '__main__':
    main()
