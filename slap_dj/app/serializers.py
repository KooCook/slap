from rest_framework import serializers

from .models import Song, Genre
from .models.artists import ArtistInSong
from .models.word import WordCache


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


class SongShortSerializer(serializers.ModelSerializer):
    artists = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Song
        fields = ('id', 'artists', 'title')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class WordOccurrenceSerializer(serializers.ModelSerializer):
    occurs_in_song = SongShortSerializer(many=True)

    class Meta:
        model = WordCache
        fields = '__all__'
