import typing

import attrs

from app.dto import commands, entities
from app.repository.reports import ReportsRepository


@typing.final
@attrs.define(slots=True, frozen=True, kw_only=True)
class ReportsService:
    _reports_repo: ReportsRepository

    async def create_report(self, *, command: commands.CreateReport) -> entities.reports.ReportDTO:
        return await self._reports_repo.create_report(command=command)
