import requests
from fastapi import FastAPI, Request,Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.api.user.services.crud import TokenCRUDService

class BlacklistTokenCheckMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, paths: list):
        super().__init__(app)
        self.paths = paths

    async def dispatch(self, request: Request, call_next):
        # Check if the request path is one of the paths to validate
        if request.url.path in self.paths:
            refresh_token = request.cookies.get("refresh_token")
            if not refresh_token:
                # If no refresh token is provided in the cookies, continue
                return await call_next(request)

            # Call the TokenCRUDService to check if the token is revoked
            # TODO: This could be offloaded to a separate service i guess
            async with TokenCRUDService() as service:
                revoked_token = await service.find_by_token(token=refresh_token)
                if revoked_token:
                    # If the token is revoked, delete the cookies
                    response = Response(content="Token is invalid", status_code=requests.codes.FORBIDDEN)
                    response.delete_cookie(key="access_token")
                    response.delete_cookie(key="refresh_token")
                    return response

        # If token is not revoked, continue with the request
        response = await call_next(request)
        return response
