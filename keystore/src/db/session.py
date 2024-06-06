from core.config import settings  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # noqa
from sqlalchemy.orm import sessionmaker

url = settings.POSTGRES_DSN

engine = create_async_engine(
    str(url),
    future=True,
    echo=False,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
