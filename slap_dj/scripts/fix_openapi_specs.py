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


def read_yaml(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        dct = yaml.load(f, yaml.FullLoader)
    return dct


def replace_info_section(specs_dct: dict, info: InfoObject) -> dict:
    specs_dct['info'] = info.as_dict()


if __name__ == '__main__':
    info = InfoObject(title='SLAP API', version='1.0.0')
