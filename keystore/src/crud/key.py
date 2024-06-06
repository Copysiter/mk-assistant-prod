from typing import Optional

from core.security import keygen  # noqa
from crud.base import CRUDBase  # noqa
from models import Key  # noqa
from schemas import KeyCreate, KeyUpdate  # noqa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDKey(CRUDBase[Key, KeyCreate, KeyUpdate]):
    async def get_by_hash(self, db: AsyncSession, *, hash: str) -> Optional[Key]:
        statement = select(Key).where(Key.hashed_key == hash)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()


key = CRUDKey(Key)
