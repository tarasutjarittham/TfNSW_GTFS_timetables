from sqlalchemy import Column
from sqlalchemy.types import Date, String, DateTime

from gtfsdb import config
from gtfsdb.model.base import Base


class FeedInfo(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'feed_info.txt'

    __tablename__ = 'feed_info'

    feed_publisher_name = Column(String(255), primary_key=True)
    feed_publisher_url = Column(String(255), nullable=False)
    feed_lang = Column(String(255), nullable=False)
    feed_start_date = Column(Date)
    feed_end_date = Column(Date)
    feed_version = Column(String(255))
    feed_license = Column(String(255))
    transport_mode = Column(String(50), primary_key=True)
    date_modified = Column(DateTime(timezone=True), primary_key=True)
