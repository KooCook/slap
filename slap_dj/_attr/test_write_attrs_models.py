import unittest
from typing import List

from utils.misc import kwds

from _attr.write_attrs_models import write_attrib, write_attrs
from app.services.youtube.models import PageInfo


class WriteAttrsModelsTestCase(unittest.TestCase):
    def test_write_attrs(self):
        json_model = """
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
        expected = """
@attr.s(kw_only=True)
class VideoListResponse:
    kind: str = attr.ib(validator=[attr.validators.instance_of(str), _attr.v.equal_to("youtube#videoListResponse")])
    etag: str = attr.ib(validator=[attr.validators.instance_of(str)])
    pageInfo: PageInfo = attr.ib(converter=_attr.c.from_dict(PageInfo), validator=[attr.validators.instance_of(PageInfo)])
    items: List[VideoResource] = attr.ib(
        converter=_attr.c.iterate(_attr.c.from_dict(VideoResource)),
        validator=[attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(VideoResource),
            iterable_validator=attr.validators.instance_of(list),
        )]
    )
    nextPageToken: str = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))
    prevPageToken: str = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))
        """.strip()
        actual = write_attrs(json_model)
        self.assertEqual(actual, expected)

    def test_write_attrib(self):
        test_cases = [
            ("    kind: str = attr.ib(validator=[attr.validators.instance_of(str), _attr.v.equal_to('youtube#videoListResponse')])",
             kwds(attrib='kind', cls=str, validate=True, equal_to='youtube#videoListResponse')),
            ('    etag: str = attr.ib(validator=[attr.validators.instance_of(str)])',
             kwds(attrib='etag', cls=str, validate=True)),
            ('    pageInfo: PageInfo = attr.ib(converter=_attr.c.from_dict(PageInfo), validator=[attr.validators.instance_of(PageInfo)])',
             kwds(attrib='pageInfo', cls=PageInfo, convert=True, validate=True)),
            ('    items: List[VideoResource] = attr.ib(converter=_attr.c.iterate(_attr.c.from_dict(VideoResource)), validator=[attr.validators.deep_iterable(member_validator=attr.validators.instance_of(VideoResource), iterable_validator=attr.validators.instance_of(list))])',
             kwds(attrib='items', cls=List['VideoResource'], convert=True, validate=True)),
            ('    nextPageToken: str = attr.ib(default=None, validator=attr.validators.optional([attr.validators.instance_of(str)]))',
             kwds(attrib='nextPageToken', cls=str, convert=True, validate=True, optional=True)),
            ('    prevPageToken: str = attr.ib(default=None, validator=attr.validators.optional([attr.validators.instance_of(str)]))',
             kwds(attrib='prevPageToken', cls=str, convert=True, validate=True, optional=True)),
        ]
        for expected, input_ in test_cases:
            with self.subTest(f"{expected=} {input_=}"):
                actual = write_attrib(**input_)
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
