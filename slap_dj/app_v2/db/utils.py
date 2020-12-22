from itertools import combinations
from typing import Type, TypeVar, List, Any, Dict

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models, IntegrityError

_M = TypeVar('_M', bound=models.Model)


def update(instance: _M, kwargs: Dict[str, Any]) -> _M:
    """ Updates and returns a Django model instance.

    Args:
        instance: An instance of a Django model.
        kwargs: A dict of {attribute: value} to update the instance with.

    Raises
        django.db.utils.IntegrityError:
            From instance.save() when failing constraints.
    """
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance


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

    err = ValueError(f"Failed to upsert cls={cls} with values uniques={uniques} rest={rest}")

    if uniques:
        try:
            oldinst = cls.objects.get(**uniques)
            return update(oldinst, rest)
        except MultipleObjectsReturned as e:
            # BAD DATA
            raise err from e
            # raise
            # try:
            #     instance = cls.objects.get(**kwargs)
            # except ObjectDoesNotExist:
            #     instances = cls.objects.filter(**uniques)
            #     # TODO: Try possible combinations from the strictest to the least strict
            #     instance = instances.first()
        except ObjectDoesNotExist:
            newinst = cls()
    else:
        assert rest == kwargs
        try:
            oldinst = cls.objects.get(**kwargs)
            return oldinst
        except ObjectDoesNotExist:
            newinst = cls()

    try:
        return update(newinst, kwargs)
    except IntegrityError as e:
        raise err from e
