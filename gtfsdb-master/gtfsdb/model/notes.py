from sqlalchemy import Column,  Sequence
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship

from gtfsdb import config
from gtfsdb.model.base import Base


class Notes(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'notes.txt'

    __tablename__ = 'notes'

    note_id = Column(String(255),primary_key=True, index=True, nullable=False)
    note_text = Column(String(255))


    stop_times = relationship(
        'StopTime',
        primaryjoin='Notes.note_id==StopTime.stop_note',
        foreign_keys='(Notes.note_id)',
        uselist=True, viewonly=True)

    trips = relationship(
        'Trip',
        primaryjoin='Notes.note_id==Trip.trip_note',
        foreign_keys='(Notes.note_id)',
        uselist=True, viewonly=True)
