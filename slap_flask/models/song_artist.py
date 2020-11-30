from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from slap_flask.database import db


class SongArtistAssociation(db.base.Model):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(String, ForeignKey('song._id'))
    artist_id = Column(String, ForeignKey('artist._id'))
    song = relationship("Song")
    artist = relationship("Artist")
    name = Column(String)

    def save(self):
        db.base.session.add(self)
        db.base.session.commit()

    def as_dict(self) -> dict:
        return { 'name': self.name }
