from db.base_class import Base  # noqa
from sqlalchemy import Boolean, Column, DateTime, Integer, String  # noqa


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    date = Column(DateTime, index=True)
    channel_name = Column(String)
    channel_url = Column(String)
