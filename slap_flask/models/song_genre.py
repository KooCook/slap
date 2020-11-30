from sqlalchemy import Column, Integer, String

from ..database import db


class SongGenre(db.base.Model):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(String)
    genre = Column(String)
