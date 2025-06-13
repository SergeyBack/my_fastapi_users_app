from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from core.config import settings
from core.models import db_helper, Base
from api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
        async with db_helper.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        yield
        await db_helper.dispose()

app = FastAPI(
        lifespan=lifespan
)
app.include_router(
        api_router,
        prefix = settings.api.prefix
        )



if __name__ =="__main__":
        uvicorn.run("main:app", 
                    host =settings.run.host,
                    port = settings.run.port,
                    reload=True,
                    )