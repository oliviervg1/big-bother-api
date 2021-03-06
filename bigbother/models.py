from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    people = relationship('Person', back_populates='room')


class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    last_seen = Column(DateTime, default=None)
    rekognition_face_id = Column(String(100), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), default=None)

    room = relationship('Room', back_populates='people')
