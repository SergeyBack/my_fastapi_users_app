from fastapi import APIRouter, Request
from core.utils.templates import templates   
from views.users.views import router as users_router

router = APIRouter()
@router.get("/", name="home")
def index_page(
        request: Request,
):
        return templates.TemplateResponse(
        request=request, 
        name="index.html",
    )


router.include_router(users_router)


