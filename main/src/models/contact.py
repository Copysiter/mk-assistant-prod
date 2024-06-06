from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import Boolean, Column, Integer, String, Text  # noqa
from sqlalchemy.orm import relationship


class Contact(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contacts = Column(String)
    specialization = Column(String, index=True)
    services = Column(String)
    location = Column(String, index=True)
    website = Column(String)
    referer = Column(String, index=True)
    comment = Column(Text)
