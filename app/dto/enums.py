import enum
import typing


@typing.final
@enum.unique
class ToneOfVoice(enum.StrEnum):
    NEUTRAL = "neutral"
    OPTIMISTIC = "optimistic"
    FRIENDLY = "friendly"
    JOKING = "joking"
    SYMPATHETIC = "sympathetic"
    ASSERTIVE = "assertive"
    FORMAL = "formal"
