from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from core.models import User
from core.schemas.user import UserCreate


async def get_all_users(
    session: AsyncSession
    )->Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user(
    session: AsyncSession,
    user_id: int,
    )->User | None:
    return await session.get(User, user_id)


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) ->User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user