from typing import TYPE_CHECKING

from db.base_class import Base  # noqa
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,  # noqa
                        String)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .key import Key  # noqa: F401


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    description = Column(String(255))
    permissions = Column(ARRAY(String(20)), nullable=False, default=[])
    is_active = Column(Boolean(), default=True, index=True)
    is_global = Column(Boolean(), default=False, index=True)

    keys = relationship("Key", back_populates="role")
