from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import Boolean, Column, Integer, String  # noqa
from sqlalchemy.orm import relationship


class Place(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    location = Column(String, index=True)
    address = Column(String)
    contacts = Column(String)
    website = Column(String)
    instagram = Column(String)
    referer = Column(String, index=True)
    comment = Column(String)
