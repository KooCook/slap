from collections import Iterable
from typing import Union, List

import requests

from settings import YOUTUBE_DATA_API_KEYS

API_KEYS = YOUTUBE_DATA_API_KEYS
CATEGORY_ID = 10

CURRENT_KEY_INDEX = 0
REGION_CODE = 'US'


def get_suitable_api_key() -> str:
    return API_KEYS[CURRENT_KEY_INDEX]


def get_youtube_video_by_ids(video_ids: Union[List[str], str]) -> List[dict]:
    """Sends a request to YouTube endpoint: 'Videos: list'.

    Args:
        video_ids: A single id or multiple ids

    Returns:


    References:
        https://developers.google.com/youtube/v3/docs/videos/list
    """
    if isinstance(video_ids, List):
        try:
            v_ids = ",".join(video_ids)
        except TypeError as e:
            raise TypeError("'video_ids' must be Iterable[str].") from e
    elif isinstance(video_ids, str):
        v_ids = video_ids
    else:
        raise TypeError(f"'video_ids' must be Iterable[str] or a CSV str, not '{video_ids.__class__.__name__}'")
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/videos', {
            'part': 'statistics,snippet',
            'videoCategoryId': CATEGORY_ID,
            'id': v_ids,
            'maxResults': 50,
            'key': get_suitable_api_key()
        }
    )
    return response.json()['items']
