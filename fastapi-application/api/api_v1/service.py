from fastapi import APIRouter

from core.config import settings

from middlewares.requests_count_middleware import request_count_middleware_dispatch

router = APIRouter(
    prefix=settings.api.v1.service,
    tags = ["Service"]
    
)


@router.get("/stats")
def get_paths_stats(
     
):
    return {
        path: {
            "count": stats.count,
            "statuses": dict(stats.statuses_counts)
        }
        for path, stats in request_count_middleware_dispatch.counts.items()
    }

