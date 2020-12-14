import unittest
from typing import List

from utils.misc import kwds

from _attr.write_attrs_models import write_attrib
from app.services.youtube.models import PageInfo


class WriteAttrsModelsTestCase(unittest.TestCase):
    def test_write_attrib(self):
        test_cases = [
            (f"    kind: str = attr.ib(validator=[attr.validators.instance_of(str), _attr.v.equal_to('youtube#videoListResponse')])",
             kwds(attrib='kind', cls=str, validate=True, equal_to='youtube#videoListResponse')),
            (f'    etag: str = attr.ib(validator=[attr.validators.instance_of(str)])',
             kwds(attrib='etag', cls=str, validate=True)),
            (f'    pageInfo: PageInfo = attr.ib(converter=_attr.c.from_dict(PageInfo), validator=[attr.validators.instance_of(PageInfo)])',
             kwds(attrib='pageInfo', cls=PageInfo, convert=True, validate=True)),
            (f'    items: List[VideoResource] = attr.ib(converter=_attr.c.iterate(_attr.c.from_dict(VideoResource)), validator=[attr.validators.deep_iterable(member_validator=attr.validators.instance_of(VideoResource), iterable_validator=attr.validators.instance_of(list))])',
             kwds(attrib='pageInfo', cls=List['VideoResource'], convert=True, validate=True)),
            (f'    nextPageToken: str = attr.ib(default=None, validator=attr.validators.optional([attr.validators.instance_of(str)]))',
             kwds(attrib='nextPageToken', cls=str, convert=True, validate=True, optional=True)),
            (f'    prevPageToken: str = attr.ib(default=None, validator=attr.validators.optional([attr.validators.instance_of(str)]))',
             kwds(attrib='prevPageToken', cls=str, convert=True, validate=True, optional=True)),
        ]
        for expected, input_ in test_cases:
            with self.subTest(f"{expected=} {input_}"):
                actual = write_attrib(**input_)
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
