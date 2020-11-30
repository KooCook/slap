from sqlalchemy import Column, Integer, String, ForeignKey

from ..database import db


class SongGenreAssociation(db.base.Model):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(String, ForeignKey('song._id'))
    song_genre = Column(String, ForeignKey('artist._id'))
