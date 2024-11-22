import typing

import attrs

from app.dto import commands, entities
from app.lib.chatgpt import ChatGPTClient
from app.lib.clusters import ClustersClient
from app.lib.wb import WBClient


@typing.final
@attrs.define(slots=True, frozen=True, kw_only=True)
class ReportsRepository:
    _chat_gpt_client: ChatGPTClient
    _wb_client: WBClient
    _clusters_client: ClustersClient

    async def create_report(
        self,
        *,
        command: commands.CreateReport,
    ) -> entities.reports.ReportDTO:
        description_command = commands.GenerateDescription.from_create_report(command=command)

        return entities.reports.ReportDTO(
            description=await self._chat_gpt_client.generate_description(command=description_command),
            clusters_num=await self._clusters_client.get_clusters_num(keywords=command.keywords),
            wb_count=await self._wb_client.get_wbcon_count(keywords=command.keywords),
        )
