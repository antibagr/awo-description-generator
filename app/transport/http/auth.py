import typing

import fastapi
import fastapi.security

from app.dto import exceptions


@typing.final
class Auth(fastapi.security.HTTPBearer):
    async def __call__(self, request: fastapi.Request) -> fastapi.security.HTTPAuthorizationCredentials | None:
        try:
            return await super().__call__(request)
        except fastapi.HTTPException as exc:
            raise exceptions.AuthenticationError(detail="Could not validate credentials") from exc


security: typing.Final = Auth()


def bearer_token(
    credentials: typing.Annotated[fastapi.security.HTTPAuthorizationCredentials, fastapi.Security(security)],
) -> str:
    """Extract the bearer token from the request."""
    return credentials.credentials
