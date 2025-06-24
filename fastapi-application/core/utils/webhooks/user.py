import time
import aiohttp

import logging

from core.schemas.user import UserRead, UserRegisteredNotification
from core.models import User

log = logging.getLogger(__name__)

WEBHOOK_URL = "https://httpbin.org/post"

async def send_new_user_notofication(user: User) -> None:
    wh_data = UserRegisteredNotification(
        user=UserRead.model_validate(user),
        ts=int(time.time())
    ).model_dump()
    log.info("Notify user created with data %s", wh_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json =wh_data) as response:
            data = await response.json()
            log.info("Sent webhook, got response: %s", data)