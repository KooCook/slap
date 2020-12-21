from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from app_v2.models import Song
from contract_models.youtube import YouTubeVideoModel


class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=255, unique=True,
                                blank=False)
    title = models.CharField(max_length=255, null=True)
    view_count = models.BigIntegerField(null=True)
    like_count = models.BigIntegerField(null=True)
    dislike_count = models.BigIntegerField(null=True)
    favorite_count = models.BigIntegerField(null=True)
    comment_count = models.BigIntegerField(null=True)
    default_language = models.CharField(max_length=10, null=True)
    published_at = models.DateTimeField(null=True)
    channel_title = models.CharField(max_length=255, null=True)
    channel = models.ForeignKey('YoutubeChannel', on_delete=models.SET_NULL, null=True)

    @classmethod
    def update_all_video_stats(cls, start=0):
        all_vid_count = cls.objects.all().count()
        current = start
        while current < all_vid_count:
            end = current + YouTubeVideoModel.HARD_LIMIT
            models = YouTubeVideoModel.from_video_ids(list(dct['video_id'] for dct in cls.objects.all()[current: end].
                                                           values('video_id')))
            for m in models:
                inst = cls.objects.get(video_id=m.video_id)
                inst.update_stats(m)
            current += YouTubeVideoModel.HARD_LIMIT

    @classmethod
    def upsert_video(cls, video_id: str, song: Song, **kwargs) -> 'YoutubeVideo':
        try:
            video = YoutubeVideo.objects.get(video_id=video_id)
        except ObjectDoesNotExist:
            video = YoutubeVideo(video_id=video_id, song=song, **kwargs)
            try:
                video.save()
            except IntegrityError as e:
                print(f'Fail {video.title} {song.title} - {e}')
        # video.update_stats()
        return video

    def update_stats(self, yt_video = None):
        if yt_video is None:
            yt_video = YouTubeVideoModel.from_video_id(self.video_id)
        if not self.title:
            self.title = yt_video.title
        self.view_count = yt_video.view_count
        self.like_count = yt_video.like_count
        self.favorite_count = yt_video.favorite_count
        self.dislike_count = yt_video.dislike_count
        self.comment_count = yt_video.comment_count
        self.published_at = yt_video.published_at
        self.channel_title = yt_video.channel_title
        self.channel_id = yt_video.channel_id
        self.default_language = yt_video.default_language
        self.save()


class YoutubeChannel(models.Model):
    title = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)

