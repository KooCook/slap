from sqlalchemy import Column, Integer, String

from ..database import db


class Artist(db.base.Model):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def as_dict(self) -> dict:
        return {'name': self.name}
