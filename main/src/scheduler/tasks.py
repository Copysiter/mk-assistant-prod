import logging
import asyncio
import aiohttp

from datetime import datetime, timedelta
from qdrant_client.models import Distance, VectorParams

from instances import qdrant_aclient
from .helpers import save_messages, save_events

BASE_URL = "http://10.60.8.62:8080/api/"
EVENTS_URL = f"{BASE_URL}events/get-all-events"
GROUPS_URL = f"{BASE_URL}channel-groups/get-all"
CHANNELS_URL = f"{BASE_URL}channels/get-by-group"
MESSAGES_URL = f"{BASE_URL}channels/get-message-history"
API_KEY = "!123ai123"

logger = logging.getLogger("apscheduler.executors.default")


async def import_channels():
    async with aiohttp.ClientSession() as session:
        result = []
        ids = []
        async with session.get(GROUPS_URL, headers={"Auth": API_KEY}) as response:
            ids = [x.get("id") for x in await response.json()]
        for id_ in ids:
            async with session.get(
                CHANNELS_URL, headers={"Auth": API_KEY}, params={"channelGroupId": id_}
            ) as response:
                result.extend(await response.json())
        logger.debug(result)


async def import_events():
    async with aiohttp.ClientSession() as session:
        async with session.get(EVENTS_URL,
                               headers={"Auth": API_KEY}) as response:
            logger.debug(await response.json())
            await save_events(await response.json())


async def import_messages():
    date = datetime.utcnow() - timedelta(days=1)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            MESSAGES_URL,
            headers={"Auth": API_KEY},
            params={"offsetDateTime": date.strftime("%Y-%m-%dT%H:%M:%S")},
        ) as response:
            logger.debug(await response.json())
            await save_messages(await response.json())


async def clear_semantic_cashe():
    await qdrant_aclient.recreate_collection(
        collection_name="semantic_cache",
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE,
        ),
    )


def run_minutely_tasks():
    pass


def run_hourly_tasks():
    pass


def run_daily_tasks():
    asyncio.run(import_events())
    asyncio.run(import_channels())
    asyncio.run(import_messages())
    asyncio.run(clear_semantic_cashe())
