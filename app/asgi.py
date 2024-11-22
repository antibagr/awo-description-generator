import fastapi
from loguru import logger

from app import logs
from app.services import service
from app.settings import settings
from app.transport import http


def register_bootstrap(_app: fastapi.FastAPI) -> None:
    _app.add_event_handler("startup", _startup)
    _app.add_event_handler("shutdown", _shutdown)


logs.setup_logging(debug=settings.DEBUG)


async def _startup() -> None:
    try:
        await service.startup()
    finally:
        logger.debug("web_server_startup")


async def _shutdown() -> None:
    try:
        await service.shutdown()
    finally:
        logger.debug("web_server_shutdown")


def get_app() -> fastapi.FastAPI:
    _app = fastapi.FastAPI(
        debug=settings.DEBUG,
        default_response_class=fastapi.responses.ORJSONResponse,
        title="AWO Generator",
    )
    register_bootstrap(_app)
    http.setup_exception_handlers(_app)
    http.register_middlewares(_app)
    http.register_http_routes(_app)
    return _app


fastapi_app = get_app()
