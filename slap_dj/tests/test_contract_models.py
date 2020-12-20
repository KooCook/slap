import unittest

from contract_models.genius import GeniusSongModel
from contract_models.youtube import YouTubeVideoModel


class ContractModelTest(unittest.TestCase):
    from app.init import start_django_lite
    start_django_lite()

    def test_yt_model(self):
        m = YouTubeVideoModel.from_video_ids(
            ['54zpFh0KuK0', 'GJSm_QMO6zA'])
        print(m)

    def test_single_artist_song(self):
        s = GeniusSongModel.from_title_and_artist("Look What You Made Me Do", "Taylor Swift")
        self.assertEqual(s.title, "Look What You Made Me Do")
        self.assertEqual(s.primary_artist.name, "Taylor Swift")

    def test_featured_artist_song(self):
        s = GeniusSongModel.from_title_and_artist("The Monster", "Eminem")
        self.assertEqual(s.title, "The Monster")
        self.assertEqual(s.primary_artist.name, "Taylor Swift")

    def test_multiple_artist_collab_song(self):
        s = GeniusSongModel.from_title_and_artist("Senorita", "Shawn Mendes")
        self.assertEqual(s.title, "Señorita")
        self.assertEqual(s.primary_artist.name, "Shawn Mendes & Camila Cabello")
