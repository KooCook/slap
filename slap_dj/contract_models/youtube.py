from dataclasses import dataclass
from typing import List

from services.youtube import get_youtube_video_by_ids


@dataclass
class YouTubeVideoModel:
    title: str = ''
    video_id: str = ''
    view_count: int = None
    like_count: int = None
    dislike_count: int = None
    favorite_count: int = None
    comment_count: int = None
    default_language: str = ''
    published_at: str = ''
    channel_id: str = ''
    channel_title: str = ''
    HARD_LIMIT = 50

    @classmethod
    def _from_dict(cls, video_id: str, dct: dict) -> 'YouTubeVideoModel':
        snippet = dct['snippet']
        published_at = snippet['publishedAt']
        stats = dct['statistics']
        lang = snippet.get('defaultAudioLanguage', snippet.get('defaultLanguage', None))
        return cls(video_id=video_id,
                title=snippet['title'],
                view_count=int(stats['viewCount']),
                like_count=int(stats.get('likeCount', 0)),
                dislike_count=int(stats.get('dislikeCount', 0)),
                favorite_count=int(stats.get('favoriteCount', 0)),
                comment_count=int(stats['commentCount']),
                published_at=published_at,
                default_language=lang,
                channel_id=snippet['channelId'],
                channel_title=snippet['channelTitle'])

    @classmethod
    def from_video_id(cls, vid_id: str) -> 'YouTubeVideoModel':
        g = get_youtube_video_by_ids(vid_id)[0]
        print(g)
        return cls._from_dict(vid_id, g)

    @classmethod
    def from_video_ids(cls, vids: List[str]) -> List['YouTubeVideoModel']:
        joined_vids = ','.join(vids)
        lst_dct: List[dict] = get_youtube_video_by_ids(joined_vids)
        return [cls._from_dict(dct['id'], dct) for dct in lst_dct]
