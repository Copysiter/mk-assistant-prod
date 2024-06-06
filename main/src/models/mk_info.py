from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import Column, Integer, String  # noqa


class MkInfo(Base):
    id = Column(Integer, primary_key=True)
    history = Column(String)
