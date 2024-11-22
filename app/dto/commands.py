"""Commands are emitted by the application layer and are consumed by the domain layer.

A command is a way to encapsulate a request to perform an action or a change in the system.
Commands are used to communicate between the application layer and the domain layer.

Commands are immutable and should be serializable to JSON if needed.
"""

from app.dto.entities.base import BaseModel


class CreateReport(BaseModel):
    """Command emitted when the user requests a new report."""

    product_name: str
    length: str
    tone_of_voice: int
    keywords: list[str]
    minus_words: list[str]
    advantages: list[str]


class GenerateDescription(BaseModel):
    """Command emitted when the user requests to generate a description."""

    product_name: str
    length: str
    tone_of_voice: int
    keywords: str
    minus_words: str
    advantages: str

    @classmethod
    def from_create_report(cls, command: CreateReport) -> "GenerateDescription":
        return cls(
            product_name=command.product_name,
            length=command.length,
            tone_of_voice=command.tone_of_voice,
            keywords=" ".join(command.keywords),
            minus_words=" ".join(command.minus_words),
            advantages=" ".join(command.advantages),
        )
