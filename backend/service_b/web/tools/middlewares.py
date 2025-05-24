import json
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware


class SetResponseStatusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response_body = b""

        async for chunk in response.body_iterator:
            response_body += chunk

        response_json = json.loads(response_body.decode("utf-8"))
        status = response_json.get("status")

        modified_response = json.dumps(response_json).encode("utf-8")
        response.headers['Content-Length'] = str(len(modified_response))

        return Response(
            content=json.dumps(response_json).encode("utf-8"),
            status_code=status if status else response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
