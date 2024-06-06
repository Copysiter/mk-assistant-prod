from datetime import datetime
from db.session import async_session
import crud, schemas  # noqa


async def save_messages(rows):
    async with async_session as db:
        for row in rows:
            await crud.message.create(db, schemas.MessageCreate(
                    ext_id=row.get('id'),
                    message_id=row.get('messageId'),
                    chat_id=row.get('channelChatId'),
                    user_id=row.get('userChatId'),
                    text=row.get('messageText'),
                    sent_ae=datetime.strptime(
                        row.get('sendingDateTime'),
                        forma='%Y-%m-%dT%H:%M:%S'
                    )
                )
            )


async def save_events(rows):
    async with async_session as db:
        for row in rows:
            await crud.event.create(db, schemas.EventCreate(
                    ext_id=row.get('id'),
                    message_id=row.get('messageId'),
                    chat_id=row.get('channelChatId'),
                    user_id=row.get('userChatId'),
                    text=row.get('messageText'),
                    sent_ae=datetime.strptime(
                        row.get('sendingDateTime'),
                        forma='%Y-%m-%dT%H:%M:%S'
                    )
                )
            )
