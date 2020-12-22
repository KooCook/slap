import unittest

from lyricsgenius.genius import Genius

from services.spotify import search_for_artist_id, search_for_song, sp


class DooddataTest(unittest.TestCase):

    def test_start(self):
        g = Genius.from_title_and_artist('So What', 'P!nk')
        g
        print(search_for_song('So What', 'P!nk'))
        a = search_for_artist_id('Pink')
        print(a)
