# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import json
import os
import csv
from typing import Union, List

import googleapiclient.discovery
import googleapiclient.errors
from dirs import ROOT_DIR
from settings import YOUTUBE_DATA_API_KEYS

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

API_KEYS = YOUTUBE_DATA_API_KEYS

CURRENT_KEY_INDEX = 0
REGION_CODE = 'US'
CATEGORY_ID = 10


def get_suitable_api_key() -> str:
    return API_KEYS[CURRENT_KEY_INDEX]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

try:
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=get_suitable_api_key())
except googleapiclient.HttpError:
    CURRENT_KEY_INDEX += 1


def main():
    with open(ROOT_DIR / 'tests/data/youtube/youtube_search_top_views_year.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'title', 'channel_id', 'publishedAt'])
        for i in range(2006, 2021):
            request = youtube.search().list(part="snippet", videoCategoryId=10, type='video', order='viewCount',
                                            publishedAfter=f"{i}-01-01T00:00:00Z",
                                            publishedBefore=f"{i+1}-01-01T00:00:00Z",
                                            regionCode=REGION_CODE,
                                            maxResults=200)
            response = request.execute()
            for x in response['items']:
                v_id = x['id']['videoId']
                title = x['snippet']['title']
                channel_id = x['snippet']['channelId']
                pub_at = x['snippet']['publishedAt']
                writer.writerow([v_id, title, channel_id, pub_at])


FILE_PATH = str(ROOT_DIR / f'tests/data/youtube/youtube_most_pop_video_{REGION_CODE}.json')


def get_youtube_video_by_ids(video_ids: Union[List[str], str]) -> List[dict]:
    """

    Args:
        video_ids: A single id or multiple ids

    Returns:

    """
    if isinstance(video_ids, list):
        v_ids = ",".join(video_ids)
    elif isinstance(video_ids, str):
        v_ids = video_ids
    else:
        raise ValueError("Error!")
    request = youtube.videos().list(part='statistics,snippet', videoCategoryId=CATEGORY_ID,
                                    id=v_ids, maxResults=10000)
    return request.execute()['items']


def get_youtube_video_list_most_popular(region_code: str):
    kwargs = {}
    scrolling = True
    next_page_token = None
    responses = []
    while scrolling:
        if next_page_token is not None:
            kwargs['pageToken'] = next_page_token
            # scrolling = False
        request = youtube.videos().list(part='statistics,snippet,contentDetails',
                                        regionCode=region_code, videoCategoryId=CATEGORY_ID,
                                        chart='mostPopular', maxResults=10000,
                                        **kwargs)
        response = request.execute()
        responses.extend(response['items'])
        for x in response['items']:
            snippet = x['snippet']
            stats = x['statistics']
            print("Retrieving...")
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            print(response)
            break
    print(json.dumps(responses), file=open(FILE_PATH, 'w'))


def read_dumped_json_to_csv(region_code: str):
    with open(FILE_PATH, 'r') as f:
        s = f.read()
        lst = json.loads(s)
        with open(ROOT_DIR / f'tests/data/youtube/api/youtube_videos_most_pop_{region_code}.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['id', 'title', 'publishedAt', 'channelId', 'channelTitle', 'viewCount',
                             'likeCount', 'dislikeCount', 'favoriteCount', 'commentCount', 'duration',
                             'defaultLanguage', 'defaultAudioLanguage'])
            for item in lst:
                sn = item['snippet']
                pub_at = sn['publishedAt']
                ch_id = sn['channelId']
                ti = sn['title']
                ch_ti = sn['channelTitle']
                stats = item['statistics']
                vc = stats['viewCount']
                lc = stats['likeCount']
                dc = stats['dislikeCount']
                fc = stats['favoriteCount']
                cc = stats['commentCount']
                v_id = item['id']
                cd = item['contentDetails']['duration']
                dl = sn.get('defaultLanguage', "")
                dal = sn.get('defaultAudioLanguage', "")
                writer.writerow([v_id, ti, pub_at, ch_id, ch_ti, vc, lc, dc, fc, cc, cd, dl, dal])


if __name__ == "__main__":
    get_youtube_video_list_most_popular(REGION_CODE)
    # read_dumped_json_to_csv(REGION_CODE)
