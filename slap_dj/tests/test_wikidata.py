import unittest

from services.wikidata import retrieve_songmodel_wikidata


class WikidataSongTest(unittest.TestCase):
    def test_retrieve_song_id(self):
        song_id = retrieve_songmodel_wikidata("Begin Again", ['Taylor Swift'])
        self.assertEqual(song_id, 'Q1708696')
        # song_id = retrieve_song_id("Begin Again", ['Taylor Swift'])
        # self.assertEqual(song_id, 'Q1708696')
