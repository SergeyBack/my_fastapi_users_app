from fastapi_users import schemas
from core.types.user_id import UserIdType
from pydantic import BaseModel

class UserRead(schemas.BaseUser[UserIdType]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserRegisteredNotification(BaseModel):
    user: UserRead
    ts: int