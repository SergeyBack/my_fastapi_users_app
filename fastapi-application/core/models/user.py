from typing import TYPE_CHECKING

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase
    )

from core.types.user_id import UserIdType

from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    
    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)