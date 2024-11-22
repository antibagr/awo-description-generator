import contextlib
import typing

from app import logs
from app.lib.chatgpt import AiohttpChatGPTClient
from app.lib.clusters import ClustersClient
from app.lib.wb import WBClient
from app.repository.reports import ReportsRepository
from app.services.liveness_probe import LivenessProbeInterface, LivenessProbeSrv
from app.services.reports import ReportsService
from app.settings import settings

# Dependencies Layer
chat_gpt_client = AiohttpChatGPTClient(
    token=settings.OPENAI_API_KEY.get_secret_value(),
    url=settings.GPT_URL,
    prompt=settings.GPT_PROMPT,
    proxy=settings.GPT_PROXY,
)

clusters_client = ClustersClient(
    url=settings.CLUSTERS_SERVICE_URL,
)

wb_client = WBClient(
    url=settings.WB_URL,
    token=settings.WB_TOKEN.get_secret_value(),
)

# Repository Layer
reports_repo = ReportsRepository(
    chat_gpt_client=chat_gpt_client,
    clusters_client=clusters_client,
    wb_client=wb_client,
)

# Service Layer
reports_service = ReportsService(reports_repo=reports_repo)


liveness_probe_resources: typing.Mapping[str, LivenessProbeInterface] = {
    "chatgpt": chat_gpt_client,
}
liveness_probe_service = LivenessProbeSrv(resources=liveness_probe_resources)


async def startup() -> None:
    logs.setup_logging(debug=settings.DEBUG)


async def shutdown() -> None: ...


@contextlib.asynccontextmanager
async def application_dependencies() -> typing.AsyncGenerator[None, None]:
    await startup()
    try:
        yield
    finally:
        await shutdown()
