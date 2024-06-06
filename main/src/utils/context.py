from instances import fastembed, qdrant


async def get_context(
    query: str, collection_name: str, limit: int, threshold: float
) -> str:
    """
    Асинхронно получает контекст для заданного запроса, используя векторизацию запроса и поиск в Qdrant.

    Функция векторизует заданный текстовый запрос и выполняет поиск по коллекции 'executors' в Qdrant,
    возвращая контекст, связанный с наиболее релевантными найденными записями.

    Параметры:
    - query (str): Текст запроса, для которого нужно найти контекст.

    Возвращает:
    - str: Строка контекста, полученная из Qdrant в ответ на запрос.
    """
    query_vector = await fastembed.embed(query)
    context = await qdrant.query(
        query_vector[0],
        collection_name=collection_name,
        payload_key="context",
        limit=limit,
        threshold=threshold,
        fast_answer=False,
    )
    return context
