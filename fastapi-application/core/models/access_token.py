from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

from .base import Base
from core.types.user_id import UserIdType

from sqlalchemy.orm import declared_attr

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):  
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "access_tokens"
    
    user_id: Mapped[UserIdType] = mapped_column(
          Integer, ForeignKey("users.id", ondelete="cascade"), 
          nullable=False,
    )
    
    
    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyAccessTokenDatabase(session, cls)