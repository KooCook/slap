import unittest

from app.model_generator import insert_song_from_model, check_song_existence
from services.wikidata import retrieve_songmodel_wikidata, retrieve_english_songs


class WikidataSongTest(unittest.TestCase):
    def test_retrieve_song_id(self):
        song_id = retrieve_songmodel_wikidata("Begin Again", ['Taylor Swift'])
        self.assertEqual(song_id, 'Q1708696')
        # song_id = retrieve_song_id("Begin Again", ['Taylor Swift'])
        # self.assertEqual(song_id, 'Q1708696')

    # def test_retrieve_songs(self):
    #     print(retrieve_english_songs())


class WikidataSongModelTest(unittest.TestCase):
    from app.init import start_django_lite
    start_django_lite()

    def test_retrieve_songs(self):
        songs = retrieve_english_songs()
        for song in songs:
            try:
                if check_song_existence(song.name, song.combined_artist_names):
                    continue
                song.update_field_data()
                insert_song_from_model(song)
            except NameError:
                pass
