import typing

import pydantic

from app.dto import annotations, enums
from app.dto.entities.base import APISchemeBaseModel


@typing.final
class CreateReportRequestPayload(APISchemeBaseModel):
    product_name: annotations.String
    length: pydantic.PositiveInt
    tone_of_voice: enums.ToneOfVoice = enums.ToneOfVoice.NEUTRAL
    keywords: list[annotations.String]
    minus_words: list[annotations.String]
    advantages: list[annotations.String]


@typing.final
class Report(APISchemeBaseModel):
    status: typing.Literal["ok"] = "ok"
    desc: str
    clusters_num: int
    wb_count: int
