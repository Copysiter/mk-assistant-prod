from datetime import datetime
from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import Column, ForeignKey, Integer, String  # noqa
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa


class Interaction(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    ext_id: Mapped[int] = mapped_column(nullable=True)
    intent: Mapped[str] = mapped_column(nullable=True)
    subintent: Mapped[str] = mapped_column(nullable=True)
    query: Mapped[str] = mapped_column(nullable=True)
    modified_query: Mapped[str] = mapped_column(nullable=True)
    result: Mapped[str] = mapped_column(nullable=True)
    logic_chain: Mapped[bool] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
