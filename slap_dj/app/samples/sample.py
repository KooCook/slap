from app.init import start_django_lite

start_django_lite()

from app.models import Artist

if __name__ == '__main__':
    Artist.generate_akas_all()
