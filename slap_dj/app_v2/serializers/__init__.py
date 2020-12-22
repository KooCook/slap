from rest_framework import serializers

from app_v2.models import Song, SpotifyGenre, Artist, ArtistSong, Word


class ArtistInSongSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="artist.name")

    class Meta:
        model = ArtistSong
        fields = ['role', 'name']


class ArtistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    artists = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    title = serializers.CharField()
    lyrics = serializers.CharField()
    # genres = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='name'
    # )

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
        model = SpotifyGenre
        fields = '__all__'


class WordOccurrenceSerializer(serializers.ModelSerializer):
    occurs_in_song = SongShortSerializer(many=True)

    class Meta:
        model = Word
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    relative_popularity = serializers.FloatField(read_only=True)

    class Meta:
        model = Word
        fields = ('word', 'relative_popularity')


class SongWithWordSerializer(serializers.ModelSerializer):
    occurs_in_song = SongShortSerializer(many=True)

    class Meta:
        model = Word
        fields = '__all__'
