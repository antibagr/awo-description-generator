import typing

from app.dto import enums
from app.dto.entities.base import APISchemeBaseModel


@typing.final
class CreateReportRequestPayload(APISchemeBaseModel):
    product_name: str
    length: str
    tone_of_voice: enums.ToneOfVoice
    keywords: list[str]
    minus_words: list[str]
    advantages: list[str]


@typing.final
class Report(APISchemeBaseModel):
    status: typing.Literal["ok"] = "ok"
    desc: str
    clusters_num: int
    wb_count: int
