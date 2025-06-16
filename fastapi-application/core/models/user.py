from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    pass
    