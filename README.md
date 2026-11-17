# Pecangaan Kulon Content API

A small FastAPI service that scrapes the public article listing and `/lapak` marketplace page from `https://pecangaankulon.jepara.go.id/`.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Endpoints

- `GET /api/articles` — article listing from the home page
- `GET /api/lapak` — marketplace listing
- `GET /health` — health check
- Add `?refresh=true` to either listing endpoint to bypass the cache

Listing responses contain `items`, `cached`, and `cache_ttl_seconds`. Each item contains `title`, `url`, `image`, `excerpt`, `date`, and `type`. The scraper sends a Chrome desktop User-Agent by default.

The in-memory cache defaults to 300 seconds. Configure it with `CACHE_TTL_SECONDS` (set to `0` to disable caching), the request timeout with `REQUEST_TIMEOUT_SECONDS`, the source host with `SOURCE_BASE_URL`, or the User-Agent with `SCRAPER_USER_AGENT`.

The cache is per process, so each worker maintains its own cache. If the source becomes unavailable after a successful fetch, the API serves the last cached result as stale data.
