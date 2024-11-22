import typing

import fastapi
import fastapi.testclient
import httpx
import pytest

from app.asgi import get_app
from app.transport.http import dependencies


@pytest.fixture(scope="session")
async def app() -> fastapi.FastAPI:
    return get_app()


@pytest.fixture()
async def client(app: fastapi.FastAPI) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url="http://test",
        transport=httpx.ASGITransport(app=app),  # type: ignore[arg-type]
    )


@pytest.fixture()
async def auth_client(
    app: fastapi.FastAPI,
    client: httpx.AsyncClient,
) -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    async def _authenticate() -> None:
        pass

    app.dependency_overrides[dependencies.authenticate] = _authenticate
    yield client
    app.dependency_overrides.clear()


# @pytest.fixture(autouse=True)
# def mock_api_response(
#     settings: Settings,
#     usdt_trc20_wallet: str,
# ) -> typing.Generator[aioresponses.aioresponses, None, None]:
#     base_url = str(settings.COIN24_API_URL)
#     with aioresponses.aioresponses() as m:
#         # ----------------------------------------
#         # COIN24 API
#         # ----------------------------------------

#         m.get(
#             make_url(base_url, "payments"),
#             payload=_coin24.get_payments,
#             repeat=True,
#         )
#         m.post(
#             make_url(base_url, "payments"),
#             payload=_coin24.create_payment,
#             repeat=True,
#         )
#         m.post(
#             make_url(base_url, "payouts"),
#             payload=_coin24.create_payout,
#             repeat=True,
#         )
#         m.post(
#             make_url(base_url, "exchanges"),
#             payload=_coin24.create_exchange,
#             repeat=True,
#         )
#         m.post(
#             make_url(base_url, "calculate-exchange"),
#             payload=_coin24.calculate_exchange,
#             repeat=True,
#         )
#         m.post(
#             make_url(base_url, "swaps"),
#             payload=_coin24.create_swap,
#             repeat=True,
#         )
#         m.get(
#             re.compile(make_url(base_url, "transaction-attributes") + r"\?.*"),
#             payload=_coin24.get_transaction_attributes,
#             repeat=True,
#         )
#         m.get(
#             re.compile(make_url(base_url, "fees") + r"\?.*"),
#             payload=_coin24.get_fees,
#             repeat=True,
#         )
#         m.get(
#             re.compile(make_url(base_url, "rates") + r"\?.*"),
#             payload=_coin24.get_rates,
#             repeat=True,
#         )

#         # ----------------------------------------
#         # KYRREX API
#         # ----------------------------------------

#         m.get(
#             make_url(str(settings.KYRREX_API_URL), "deposit-address", "usdt", "trc20usdt"),
#             payload={"address": usdt_trc20_wallet},
#             repeat=True,
#         )
#         yield m
