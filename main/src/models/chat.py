from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import Column, Integer, String  # noqa


class Chat(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    chat_id = Column(String)
    link = Column(String)
    category = Column(String)
    messenger = Column(String)
