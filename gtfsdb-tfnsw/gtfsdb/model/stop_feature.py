from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, String, DateTime

from gtfsdb import config
from gtfsdb.model.base import Base


__all__ = ['StopFeature']


class StopFeature(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'stop_features.txt'

    __tablename__ = 'stop_features'

    id = Column(Integer, Sequence(None, optional=True), primary_key=True)
    stop_id = Column(String(255), index=True, nullable=False)
    feature_type = Column(String(50), index=True, nullable=False)
    feature_name = Column(String(255))
    transport_mode = Column(String(50), primary_key=True)
    date_modified = Column(DateTime(timezone=True), primary_key=True)
