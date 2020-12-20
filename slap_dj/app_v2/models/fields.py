from typing import List
import json

from django.core.exceptions import ValidationError
from django.db import models

from django.utils.translation import gettext_lazy as _


# def parse_quantity(quantity_string: str) -> Quantity:
#     amount, *unit = quantity_string.split(' ')
#     amount = Fraction(amount)
#     try:
#         return Quantity(amount, ' '.join(unit))
#     except ValueError as e:
#         raise ValidationError(_("Invalid input for a Quantity instance")
#                               ) from e


class CSVField(models.CharField):
    description = _("Comma-separated value")

    def db_csv_to_list(self, csv: str) -> list:
        parts = json.loads(csv)
        return list(map(self.item_type, parts))

    def list_to_db_csv(self, lst: list) -> str:
        parts = list(map(str, lst))
        return json.dumps(parts)

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1000
        self.item_type = kwargs.pop('item_type')
        self.max_length = 1000
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('max_length')
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None or value == '':
            return value
        return self.db_csv_to_list(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return value
        return self.db_csv_to_list(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.list_to_db_csv(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
