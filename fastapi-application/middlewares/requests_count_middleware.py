from collections import defaultdict
from dataclasses import dataclass, field
from fastapi import Request, Response

from typing import Awaitable, Callable


@dataclass
class PathCounts:
    count: int = 0
    statuses_counts : defaultdict[int,int] = field(
        default_factory = lambda: defaultdict(int)
    )


class RequestCountMiddlewareDispatch:
    def __init__(self):
        self.counts = defaultdict[str, PathCounts](PathCounts)
        
    async def __call__(
        self,
        request: Request,
        call_next:  Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        self.counts[path].count += 1
        try:
            response = await call_next(request)
        except Exception:
            self.counts[path].statuses_counts[999] += 1
            raise
        self.counts[path].statuses_counts[response.status_code] += 1
        return response
    
request_count_middleware_dispatch = RequestCountMiddlewareDispatch()
       