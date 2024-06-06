import crud  # noqa
import schemas
from core.config import settings  # noqa
from core.security import keygen  # noqa
from db.base_class import Base  # noqa
from db.session import async_session, engine  # noqa


# Create first superuser
async def create_global_role() -> None:
    async with async_session() as session:
        rows = await crud.role.get_rows(
            session,
            filters=[
                {
                    "field": "name",
                    "operator": "eq",
                    "value": settings.FIRST_GLOBAL_ROLE,
                },
                {"field": "is_global", "operator": "eq", "value": True},
            ],
        )
        if not rows:
            role_in = schemas.RoleCreate(
                name=settings.FIRST_GLOBAL_ROLE,
                is_global=True,
            )
            return await crud.role.create(session, obj_in=role_in)
        return rows[0]


async def create_api_key(role) -> None:
    if not role:
        return
    async with async_session() as session:
        key = await crud.key.get_rows(
            session,
            filters=[
                {"field": "role_id", "operator": "eq", "value": role.id},
                {"field": "expires_at", "operator": "isnull"},
            ],
        )
        if key:
            return key[0]
        key_in = schemas.KeyCreate(
            role_id=role.id, hashed_key=keygen.hash(settings.FIRST_API_KEY)
        )
        return await crud.key.create(session, obj_in=key_in)


# Create tables
async def init_models() -> None:
    async with engine.begin() as conn:
        if settings.DATABASE_DELETE_ALL:
            await conn.run_sync(Base.metadata.drop_all)
        if settings.DATABASE_CREATE_ALL:
            await conn.run_sync(Base.metadata.create_all)


async def init_db() -> None:
    await init_models()
    await create_api_key(await create_global_role())
