import typing

import yaml
import ruamel.yaml

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


@attr.s(slots=True)
class Attrib:
    name: str = attr.ib()
    type: typing.Union[type, type(typing.List), typing.ForwardRef] = attr.ib()
    is_optional: bool = attr.ib(default=False, converter=bool)
    default: typing.Any = attr.ib(default=None)
    converters: typing.List[str] = attr.ib(factory=list, validator=attr.validators.instance_of(list))
    validators: typing.List[str] = attr.ib(factory=list, validator=attr.validators.instance_of(list))


@attr.s(slots=True)
class Attrs:
    name: str
    attrs_kwds: dict = attr.ib(factory=dict, validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str), value_validator=[]))
    attribs: typing.List[Attrib] = attr.ib(factory=list, validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(Attrib), iterable_validator=attr.validators.instance_of(list)))

    def __str__(self):
        return f"""
@attr.s(kw_only=True)
class {self.name}:
""" + '\n'.join(map(str, self.attribs))


def main():
    from ruamel.yaml import scalarstring
    # tmp = yaml.load(template, Loader=yaml.FullLoader)
    # print(tmp)
    tmp = ruamel.yaml.round_trip_load(template, preserve_quotes=True)

    print(isinstance(tmp['etag'], scalarstring.DoubleQuotedScalarString))

    # lines = [
    #     f'@attr.s',
    #     f'class {camel_to_capwords(tmp["kind"].split("#")[1])}',
    # ]
    # for k, v in tmp.items():
    #     if isinstance(v, str):
    #         try:
    #             t = {
    #                 'string': str,
    #                 'integer': int,
    #                 'decimal': float,
    #             }[v]
    #         except KeyError:
    #             pass

        # write_attrib(k, )
    # lsAt = [
    #     f'     kind: str = attr.ib(validator=[attr.validators.instance_of(str), attr.v.equal_to("youtube#videoListResponse")])',
    #     f'     etag: str = attr.ib(validator=[attr.validators.instance_of(str)])',
    #     f'     pageInfo: PageInfo = attr.ib(converter=attr.c.from_dict(PageInfo), validator=[attr.validators.instance_of(PageInfo)])',
    #     f'     items: List[VideoResource] = attr.ib()',
    #     f'     nextPageToken: str = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))',
    #     f'     prevPageToken: str = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))',
    # ]


def write_attrs(json_model: str) -> str:
    """Returns the lines of code to write a attrs class"""
    return ''


if __name__ == '__main__':
    main()
