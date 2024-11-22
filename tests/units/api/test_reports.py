import fastapi
import httpx

from app.transport.http.api.public import reports
from app.transport.http.schema.reports import CreateReportRequestPayload


async def test_create_reports(
    app: fastapi.FastAPI,
    auth_client: httpx.AsyncClient,
) -> None:
    resp = await auth_client.post(
        app.url_path_for(reports.create_report.__name__),
        json=CreateReportRequestPayload(
            product_name="test",
            length=100,
            tone_of_voice="formal",
            keywords=["keyword"],
            minus_words=["minus"],
            advantages=["adv"],
        ).model_dump(),
    )
    assert resp.status_code == fastapi.status.HTTP_200_OK
    assert resp.json() == {
        "product_name": "test",
        "length": 1,
        "tone_of_voice": "formal",
        "keywords": ["keyword"],
        "minus_words": ["minus"],
        "advantages": ["adv"],
    }
