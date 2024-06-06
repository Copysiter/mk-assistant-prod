from datetime import datetime

from db.base_class import Base  # noqa
from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String  # noqa
from sqlalchemy.orm import Mapped, mapped_column, relationship  # noqa


class Message(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ext_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[int] = mapped_column(nullable=True)
    sent_at: Mapped[datetime] = mapped_column(nullable=True)