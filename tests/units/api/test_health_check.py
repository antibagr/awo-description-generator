import fastapi
import httpx

from app.transport.http.api.service import health


async def test_health_check_404(
    app: fastapi.FastAPI,
    client: httpx.AsyncClient,
) -> None:
    service = "nonexistent"
    resp = await client.get(app.url_path_for(health.get_service_status.__name__, service=service))
    assert resp.status_code == fastapi.status.HTTP_404_NOT_FOUND
    assert resp.json() == {
        "detail": f"Service {service} not found",
        "code": "not_found",
    }
