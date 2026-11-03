"""Issue #10 HTTP integration spike; no production adapter or private page data."""

import asyncio
import json
import platform
from importlib.metadata import version

import httpx
from fastapi import FastAPI
from tavily import AsyncTavilyClient


async def run_checks():
    """Check ASGI calls, provider-shaped responses, failures, and public GDELT."""
    results = {"python": platform.python_version(), "packages": {
        name: version(name) for name in ("fastapi", "uvicorn", "httpx", "tavily-python")
    }}
    app = FastAPI()

    @app.get("/health")
    def health_check():
        return {"status": "ok", "environment": "development"}

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),
                                 base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    results["asgi_health_spike"] = "passed (replicated scaffold route, not imported PR)"

    def provider_stub(request):
        if request.url.path == "/timeout":
            raise httpx.ReadTimeout("synthetic timeout", request=request)
        if request.url.path == "/rate-limit":
            return httpx.Response(429, json={"error": "rate limited"})
        if request.url.path == "/empty":
            return httpx.Response(200, json={})
        return httpx.Response(200, json={"claims": [{"text": "Example claim",
            "claimReview": [{"publisher": {"name": "Example publisher"},
                             "url": "https://example.org/review",
                             "textualRating": "Example rating"}]}]})

    async with httpx.AsyncClient(transport=httpx.MockTransport(provider_stub),
                                 base_url="https://provider.invalid", timeout=5) as client:
        response = await client.get("/claims", params={"query": "Example claim"})
        assert response.json()["claims"][0]["claimReview"][0]["url"]
        assert (await client.get("/empty")).json().get("claims", []) == []
        try:
            (await client.get("/rate-limit")).raise_for_status()
        except httpx.HTTPStatusError as error:
            assert error.response.status_code == 429
        else:
            raise AssertionError("429 was not surfaced")
        try:
            await client.get("/timeout")
        except httpx.ReadTimeout:
            pass
        else:
            raise AssertionError("Timeout was not surfaced")
    results["httpx_fixtures"] = "passed: claim response, empty result, 429, timeout"
    assert callable(AsyncTavilyClient.search)
    results["tavily_sdk_import"] = "passed; no authenticated call performed"

    # Fixed public topic only. Never print request URLs or provider response bodies.
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get("https://api.gdeltproject.org/api/v2/doc/doc",
                params={"query": "election", "mode": "artlist", "format": "json",
                        "maxrecords": 5, "timespan": "24h"})
            response.raise_for_status()
            articles = response.json().get("articles", [])
            assert isinstance(articles, list)
            results["gdelt_live"] = {"status": response.status_code,
                                     "article_count": len(articles)}
    except (httpx.HTTPError, ValueError, AssertionError) as error:
        results["gdelt_live"] = {"error_type": type(error).__name__,
                                 "note": "Availability failure; no quality conclusion"}
        if isinstance(error, httpx.HTTPStatusError):
            results["gdelt_live"]["status"] = error.response.status_code
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(run_checks())
