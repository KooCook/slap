from sqlalchemy import Column, Integer, String, Float

from ..database import db


class Song(db.base.Model):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    artist = Column(String)
    lyrics = Column(String)
    compressibility = Column(Float)

    def save(self):
        db.base.session.add(self)
        db.base.session.commit()
