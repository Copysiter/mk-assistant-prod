from db.base_class import Base  # noqa
from sqlalchemy import Column, Integer, String, Text  # noqa
from sqlalchemy.orm import Mapped, mapped_column


class Info(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, nullable=True, index=True)
    value: Mapped[str] = mapped_column(Text)
