from datetime import datetime
from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,  # noqa
                        String)
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .role import Role  # noqa: F401


class Key(Base):
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    name = Column(String(20))
    description = Column(String(255))
    hashed_key = Column(String(255), nullable=False, index=True)
    issued_at = Column(DateTime(), default=datetime.utcnow)
    expires_at = Column(DateTime())
    is_active = Column(Boolean(), default=True, index=True)

    role = relationship("Role", back_populates="keys", lazy="joined")
