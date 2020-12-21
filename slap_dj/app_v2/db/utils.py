from itertools import combinations
from typing import Type, TypeVar, List

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models, IntegrityError

_M = TypeVar('_M', bound=models.Model)


def get_unique_fields(cls: Type[_M]) -> List[str]:
    unique_fields: List[models.Field] = []
    for field in cls._meta.get_fields():
        if isinstance(field, models.OneToOneRel):
            pass
        elif isinstance(field, models.ManyToOneRel):
            pass
        elif isinstance(field, models.ManyToManyRel):
            pass
        else:
            if field.unique:
                unique_fields.append(field)
    return [f.name for f in unique_fields ]


def upsert(cls: Type[_M], **kwargs) -> _M:
    unique_fields = get_unique_fields(cls)
    uniques = {}
    rest = {}
    for k, v in kwargs.items():
        if k in unique_fields:
            uniques[k] = v
        else:
            rest[k] = v
    if uniques:
        try:
            instance = cls.objects.get(**uniques)
        except MultipleObjectsReturned:
            # BAD DATA
            raise
            # raise
            # try:
            #     instance = cls.objects.get(**kwargs)
            # except ObjectDoesNotExist:
            #     instances = cls.objects.filter(**uniques)
            #     # TODO: Try possible combinations from the strictest to the least strict
            #     instance = instances.first()
        except ObjectDoesNotExist:
            instance = cls()
    else:
        try:
            instance = cls.objects.get(**kwargs)
            return instance
        except ObjectDoesNotExist:
            instance = cls()
    for k, v in kwargs.items():
        setattr(instance, k, v)
    try:
        instance.save()
    except IntegrityError as e:
        raise
    return instance
