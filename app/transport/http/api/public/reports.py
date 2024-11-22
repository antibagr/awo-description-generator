import typing

import fastapi
from loguru import logger

from app.dto import commands, exceptions
from app.services.reports import ReportsService
from app.transport.http import dependencies, schema

router = fastapi.APIRouter(
    tags=["reports"],
    dependencies=[fastapi.Depends(dependencies.authenticate)],
)


@router.post(
    path="/v1/reports",
    summary="Create product report",
    responses=schema.error.Responses,
)
async def create_report(
    req: schema.reports.CreateReportRequestPayload,
    reports_service: typing.Annotated[
        ReportsService,
        fastapi.Depends(dependencies.reports_service),
    ],
) -> schema.reports.Report:
    try:
        report = await reports_service.create_report(
            command=commands.CreateReport(
                product_name=req.product_name,
                length=req.length,
                tone_of_voice=req.tone_of_voice,
                keywords=req.keywords,
                minus_words=req.minus_words,
                advantages=req.advantages,
            )
        )
        return schema.reports.Report(
            desc=report.description,
            clusters_num=report.clusters_num,
            wb_count=report.wb_count,
        )
    except Exception as exc:
        logger.opt(exception=exc).error("Error on creating product report.")
        raise exceptions.ReportGenerationError("Error on generating product description.") from exc
