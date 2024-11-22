from __future__ import annotations

import contextlib
import contextvars
import decimal
import inspect
import json
import logging
import random
import sys
import typing
import uuid

import loguru
from loguru import logger

__all__ = ["set_new_operation_id", "setup_logging"]


class _InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # noqa: PLR6301
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def custom_serializer(obj: uuid.UUID | decimal.Decimal | typing.AnyStr) -> str:
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, decimal.Decimal):
        return f"{obj:f}"
    return str(obj)


operation_id: contextvars.ContextVar[int] = contextvars.ContextVar("operation_id")
_user_id: contextvars.ContextVar[uuid.UUID] = contextvars.ContextVar("user_id")


@contextlib.contextmanager
def user_id(value: uuid.UUID) -> typing.Generator[None, None, None]:
    token = _user_id.set(value)
    try:
        yield
    finally:
        _user_id.reset(token)


def set_new_operation_id() -> int:
    op_id = random.getrandbits(128)
    operation_id.set(op_id)
    return op_id


def _get_operation_id() -> int:
    op_id: int
    try:
        op_id = operation_id.get()
    except LookupError:
        op_id = set_new_operation_id()
    return op_id


def _serialize(record: loguru.Record) -> tuple[str, bool]:
    err = False
    subset = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "operation_id": str(_get_operation_id()),
        "extra": record["extra"],
    }

    if exc := record["exception"]:
        err = True
        subset["exception"] = str(exc)

    if acc_id := _user_id.get(None):
        record["extra"]["user_id"] = acc_id

    return f"{json.dumps(subset, default=custom_serializer)}\n", err


def _sink(message: loguru.Message) -> None:
    serialized, _err = _serialize(message.record)
    sys.stdout.write(serialized)


def setup_logging(*, debug: bool) -> None:
    # TODO (rudiemeant@gmail.com): Figure out how to log exceptions
    # properly with serialization
    # https://spenx.atlassian.net/browse/DAUP-254
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logger.remove()
    # logger.add(_sink, level="DEBUG" if debug else "INFO")
    logger.add(sys.stdout, level="DEBUG" if debug else "INFO")
    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)
