import typing
from dataclasses import dataclass

import yaml
import attr


class AsDictMixin:
    def as_dict(self) -> dict:
        dct = {}
        for field in self.__slots__:
            if field:
                dct[field] = getattr(self, field)
        return dct


@attr.s(slots=True)
class InfoObject(AsDictMixin):
    title: str = attr.ib(converter=str)
    version: str = attr.ib(converter=str)
    description: str = attr.ib(default=None)
    termsOfService: str = attr.ib(default=None)
    contact: dict = attr.ib(factory=dict)
    license: dict = attr.ib(factory=dict)


@attr.s(slots=True)
class ServerObject(AsDictMixin):
    url: str = attr.ib(converter=str)
    description: str = attr.ib(default=None)
    variables: dict = attr.ib(factory=dict)


@attr.s(slots=True)
class ReferenceObject(AsDictMixin):
    ref: str = attr.ib(converter=str)


param_location_choices = ('query', 'header', 'path', 'cookie')


@attr.s(slots=True)
class ParameterObject(AsDictMixin):
    name: str = attr.ib(converter=str) # validate
    in_: str = attr.ib(converter=str, validator=attr.validators.in_(param_location_choices)) # validate
    description: str = attr.ib(default=None)
    required: bool = attr.ib(validator=attr.validators.instance_of(bool),
                             default=False)
    depreciated: bool = attr.ib(default=False)
    allowEmptyValue: bool = attr.ib(default=False)

    @name.validator
    def check_name(self, attribute, value):
        pass

    @required.validator
    def check_required(self, attribute, value):
        if self.in_ == 'path':
            if not value:
                raise ValueError("Required must be `True` if the parameter location is in 'path'")


@attr.s(slots=True)
class PathItemObject(AsDictMixin):
    ref: str = attr.ib(default=None)
    summary: str = attr.ib(default=None)
    description: str = attr.ib(default=None)
    get: OperationObject = attr.ib(default=None)
    put: OperationObject = attr.ib(default=None)
    post: OperationObject = attr.ib(default=None)
    delete: OperationObject = attr.ib(default=None)
    options: OperationObject = attr.ib(default=None)
    head: OperationObject = attr.ib(default=None)
    patch: OperationObject = attr.ib(default=None)
    trace: OperationObject = attr.ib(default=None)
    servers: typing.List[ServerObject] = attr.ib(factory=list)
    parameters: typing.List[typing.Union[ParameterObject,
                                         ReferenceObject]] = attr.ib(factory=list)


def read_yaml(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        dct = yaml.load(f, yaml.FullLoader)
    return dct


def replace_info_section(specs_dct: dict, info: InfoObject) -> dict:
    specs_dct['info'] = info.as_dict()



if __name__ == '__main__':
    info = InfoObject(title='SLAP API', version='1.0.0')
