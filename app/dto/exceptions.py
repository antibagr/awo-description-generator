import typing


class ErrorProtocol(typing.Protocol):
    detail: str
    code: str


class APIError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class ClientError(APIError):
    code = "client_error"


class AuthenticationError(APIError):
    code = "authentication_error"


class ReportGenerationError(APIError):
    code = "report_generation_error"


class NotFoundError(APIError):
    code = "not_found"
