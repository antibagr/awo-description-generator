import aiohttp
import pytest

from app.lib.chatgpt import AiohttpChatGPTClient
from app.lib.clusters import ClustersClient
from app.lib.wb import WBClient
from app.repository.reports import ReportsRepository
from app.services.reports import ReportsService
from app.settings import Settings


@pytest.fixture()
def settings() -> Settings:
    return Settings()


@pytest.fixture()
async def aiohttp_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession()


@pytest.fixture()
async def chat_gpt_client(settings: Settings) -> AiohttpChatGPTClient:
    return AiohttpChatGPTClient(
        token=settings.OPENAI_API_KEY,
        url=settings.GPT_URL,
        prompt=settings.GPT_PROMPT,
        proxy=settings.GPT_PROXY,
        model=settings.GPT_MODEL,
    )


@pytest.fixture()
async def clusters_client(settings: Settings) -> ClustersClient:
    return ClustersClient(url=settings.CLUSTERS_SERVICE_URL)


@pytest.fixture()
async def wb_client(settings: Settings) -> WBClient:
    return WBClient(url=settings.WB_URL, token=settings.WB_TOKEN.get_secret_value())


@pytest.fixture()
async def reports_repo(
    chat_gpt_client: AiohttpChatGPTClient,
    clusters_client: ClustersClient,
    wb_client: WBClient,
) -> ReportsRepository:
    return ReportsRepository(
        chat_gpt_client=chat_gpt_client,
        clusters_client=clusters_client,
        wb_client=wb_client,
    )


@pytest.fixture()
async def reports_service(
    reports_repo: ReportsRepository,
) -> ReportsService:
    return ReportsService(reports_repo=reports_repo)
