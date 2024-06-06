from db.base_class import Base  # noqa
from sqlalchemy import Column, ForeignKey, Integer, String  # noqa
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa


class Prompt(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(unique=True)
    prompt: Mapped[str]
