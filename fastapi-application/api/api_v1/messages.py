from fastapi import APIRouter
from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_user, current_superuser
    )
from core.config import settings
from core.models import User
from core.schemas.user import UserRead

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags = ["Messages"]
    
)


@router.get("")
def get_user_messages(
    user: User = Depends(current_user),
):
    return {
        "messages": ["m1"],
        "user": UserRead.model_validate(user)
    }
    
@router.get("/secrets")
def get_superuser_messages(
    user: User = Depends(current_superuser),
):
    return {
        "messages": ["secret-m1"],
        "user": UserRead.model_validate(user)
    }