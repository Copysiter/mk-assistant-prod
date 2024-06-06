from typing import Optional

import crud
from db.session import async_session


async def get_template_from_db(type: str) -> Optional[str]:
    """
    Асинхронно извлекает шаблон промпта по ключу из базы данных.

    Параметры:
        template_key (str): Ключ шаблона, который необходимо извлечь.

    Возвращает:
        Optional[str]: Шаблон как строку, если найден, иначе None.
    """
    async with async_session() as db:
        template_data = await crud.prompt.get(db, type)
        return template_data.prompt if template_data else None
