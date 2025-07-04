from contextlib import asynccontextmanager

from core import broker
from core.models import db_helper
from fastapi.responses import ORJSONResponse

from api.webhooks import webhook_router

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from errors_handlers import register_errorsr_handlers
from middlewares.middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
        #startp
        await broker.startup()
        yield
        #shutdwn
        await db_helper.dispose()
        await broker.shutdown()


def register_static_docs_routes(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url, # type: ignore
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False) # type: ignore
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url, # type: ignore
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
        )


    # @app.get("/users/{username}")
    # async def read_user(username: str):
    #     return {"message": f"Hello {username}"}


def create_app(
    create_custom_static_urls: bool =False,
    )-> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        docs_url=None if create_custom_static_urls else "/docs", 
        redoc_url= None if create_custom_static_urls else "/redoc",
        webhooks=webhook_router,
    )
    if create_custom_static_urls:
        register_static_docs_routes(app)
        
    register_errorsr_handlers(app)
    register_middlewares(app)
    return app
     