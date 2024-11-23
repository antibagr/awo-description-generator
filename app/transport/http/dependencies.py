import typing

import aiohttp
import fastapi
import fastapi.security

from app.dto import exceptions
from app.lib.chatgpt import ChatGPTClient, OpenAIChatGPTClient
from app.lib.clusters import ClustersClient
from app.lib.wb import WBClient
from app.repository.reports import ReportsRepository
from app.services.liveness_probe import LivenessProbeSrv
from app.services.reports import ReportsService
from app.settings import Settings
from app.settings import settings as global_settings
from app.transport.http import auth


def settings() -> Settings:
    return global_settings


async def aiohttp_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession()


async def chat_gpt_client(
    settings: typing.Annotated[Settings, fastapi.Depends(settings)],
) -> ChatGPTClient:
    return OpenAIChatGPTClient(
        token=settings.OPENAI_API_KEY.get_secret_value(),
        prompt=settings.GPT_PROMPT,
        proxy=settings.GPT_PROXY,
    )


async def clusters_client(
    settings: typing.Annotated[Settings, fastapi.Depends(settings)],
) -> ClustersClient:
    return ClustersClient(
        url=str(settings.CLUSTERS_SERVICE_URL),
    )


async def wb_client(
    settings: typing.Annotated[Settings, fastapi.Depends(settings)],
) -> WBClient:
    return WBClient(
        url=str(settings.WB_URL),
        token=settings.WB_TOKEN.get_secret_value(),
    )


async def reports_repo(
    chat_gpt_client: typing.Annotated[ChatGPTClient, fastapi.Depends(chat_gpt_client)],
    clusters_client: typing.Annotated[ClustersClient, fastapi.Depends(clusters_client)],
    wb_client: typing.Annotated[WBClient, fastapi.Depends(wb_client)],
) -> ReportsRepository:
    return ReportsRepository(
        chat_gpt_client=chat_gpt_client,
        clusters_client=clusters_client,
        wb_client=wb_client,
    )


async def reports_service(
    reports_repo: typing.Annotated[ReportsRepository, fastapi.Depends(reports_repo)],
) -> ReportsService:
    return ReportsService(reports_repo=reports_repo)


def liveness_resources() -> dict[str, typing.Any]:
    return {}


async def liveness_probe_service(
    liveness_resources: typing.Annotated[dict[str, typing.Any], fastapi.Depends(liveness_resources)],
) -> LivenessProbeSrv:
    return LivenessProbeSrv(resources=liveness_resources)


async def authenticate(
    token: typing.Annotated[str, fastapi.Depends(auth.bearer_token)],
    settings: typing.Annotated[Settings, fastapi.Depends(settings)],
) -> None:
    if token != settings.AUTH_TOKEN.get_secret_value():
        raise exceptions.AuthenticationError(detail="Could not validate credentials")
