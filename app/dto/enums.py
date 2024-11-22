import enum
import typing


@typing.final
@enum.unique
class ToneOfVoice(enum.Enum):
    NEUTRAL = "neutral"
    OPTIMISTIC = "optimistic"
    FRIENDLY = "friendly"
    JOKING = "joking"
    SYMPATHETIC = "sympathetic"
    ASSERTIVE = "assertive"
    FORMAL = "formal"
