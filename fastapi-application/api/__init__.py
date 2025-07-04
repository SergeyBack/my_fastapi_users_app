from fastapi import APIRouter
from .api_v1 import router as router_api_v1

from core.config import settings

router = APIRouter()
router.include_router(
    router_api_v1,
    prefix = settings.api.prefix
    )