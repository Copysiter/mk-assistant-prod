from datetime import datetime
from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy.orm import Mapped, mapped_column  # noqa


class News(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    created_at: Mapped[datetime]
