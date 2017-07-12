from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, DateTime

from gtfsdb import config
from gtfsdb.model.base import Base


class Frequency(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'frequencies.txt'

    __tablename__ = 'frequencies'

    trip_id = Column(String(255), primary_key=True)
    start_time = Column(String(8), primary_key=True)
    end_time = Column(String(8))
    headway_secs = Column(Integer)
    exact_times = Column(Integer)
    transport_mode = Column(String(50), primary_key=True)
    date_modified = Column(DateTime(timezone=True), primary_key=True)

    trip = relationship(
        'Trip',
        primaryjoin='Frequency.trip_id==Trip.trip_id',
        foreign_keys='(Frequency.trip_id)',
        uselist=False, viewonly=True)
