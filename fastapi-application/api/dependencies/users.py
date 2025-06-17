from typing import TYPE_CHECKING, Annotated
from core.models import db_helper, User

from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated[
        "AsyncSession", 
        Depends(db_helper.session_getter)
    ],
):
    yield User.get_db(session=session)

