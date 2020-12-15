from django.core.management.base import BaseCommand

from ._populate_models import generate_artists, chain_kpop_songs


class Command(BaseCommand):
    help = 'Populates the song data with associated data'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Indicates the mode of data population')

    def handle(self, *args, **kwargs):
        m = kwargs['mode']
        if m == 'kpop':
            self.stdout.write("Start kpop songs")
            chain_kpop_songs()
        elif m == 'artists':
            self.stdout.write("Start gen artist")
            generate_artists()
