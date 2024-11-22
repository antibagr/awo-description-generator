import typing

from app.dto.entities.base import BaseModel


@typing.final
class ReportDTO(BaseModel):
    description: str
    clusters_num: int
    wb_count: int
