from fastapi import APIRouter
from core.config import settings
from core.schemas.user import UserRead, UserUpdate

from .fastapi_users import fastapi_users

router = APIRouter(
    prefix=settings.api.v1.users,
    tags = ["Users"]
)
# /me
# /{id} 
router.include_router(
    router = fastapi_users.get_users_router(
        UserRead, 
        UserUpdate,
        ),
)

# from typing import Annotated

# from fastapi import APIRouter, Depends

# from sqlalchemy.ext.asyncio import AsyncSession

# from core.models import db_helper
# from core.schemas.user import UserRead, UserCreate

# from crud import users as users_crud
# from api.dependencies.authentication import authentication_backend



# @router.get("", response_model = list[UserRead])
# async def get_users(
#     session: Annotated[
#         AsyncSession, 
#         Depends(db_helper.session_getter)
#         ],
# ):
#     users = await users_crud.get_all_users(session=session)
#     return users


# @router.post("", response_model=UserRead)
# async def create_user(
#     session: Annotated[
#         AsyncSession,
#         Depends(db_helper.session_getter),
#     ],
#     user_create: UserCreate,
# ):
#     user = await users_crud.create_user(
#         session=session,
#         user_create=user_create,
#     )
#     
#     return user