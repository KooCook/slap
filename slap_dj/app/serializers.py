from rest_framework import serializers

from .models import Song
from .models.artists import ArtistInSong


class ArtistInSongSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="artist.name")

    class Meta:
        model = ArtistInSong
        fields = ['role', 'name']


class SongSerializer(serializers.ModelSerializer):
    artists = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Song
        fields = '__all__'
