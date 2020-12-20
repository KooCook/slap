from dataclasses import dataclass, field
from typing import List

from lyricsgenius.song import Song

from contract_models import Artist, ArtistRole
from services.genius import genius_client


@dataclass
class GeniusMediaLink:
    pass


@dataclass
class GeniusSongModel:
    genius_id: str = ''
    title: str = ''
    lyrics: str = ''
    artists: List[Artist] = field(default_factory=list)
    medias: List[GeniusMediaLink] = field(default_factory=list)
    image_thumbnail_url: str = ''
    image_url: str = ''
    apple_music_id: str = ''
    release_date: str = '' # 2014-03-17

    @property
    def primary_artist(self) -> Artist:
        return next(artist for artist in self.artists
                    if artist.role == ArtistRole.Primary)

    def add_primary_artist(self, artist_name: str):
        self.artists.insert(0, Artist(role=ArtistRole.Primary, name=artist_name))

    def add_featured_artist(self, artist_name: str):
        self.artists.append(Artist(role=ArtistRole.Featured, name=artist_name))

    @classmethod
    def from_title_and_artist(cls, song_name: str, artist_name: str) -> 'GeniusSongModel':
        song: Song = genius_client.search_song(song_name, artist_name)
        m = cls(lyrics=song.lyrics,
                title=song.title,
                release_date=song.year,
                image_url=song.song_art_image_url,
                genius_id=song._id)
        m.add_primary_artist(song.artist)
        for artist in song.featured_artists:
            # {'api_path': '/artists/92', 'header_image_url': 'https://images.genius.com/ab2a85c825e8e602ff228a210a218473.913x498x1.png', 'id': 92, 'image_url': 'https://images.genius.com/be1eda80c5e637a4f1450fa68408f3a2.1000x1000x1.jpg', 'is_meme_verified': True, 'is_verified': True, 'name': 'Nicki Minaj', 'url': 'https://genius.com/artists/Nicki-minaj', 'iq': 3295}
            m.add_featured_artist(artist['name'])
        print(song.featured_artists)
        return m
