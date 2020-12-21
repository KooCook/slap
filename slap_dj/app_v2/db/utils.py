from typing import Type, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

_M = TypeVar('_M', bound=models.Model)


def upsert(cls: Type[_M], **kwargs) -> _M:
    try:
        instance = cls.objects.get(**kwargs)
    except ObjectDoesNotExist:
        instance = cls(**kwargs)
        try:
            instance.save()
        except IntegrityError as e:
            raise
    return instance
