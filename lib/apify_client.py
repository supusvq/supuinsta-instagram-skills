"""Thin Apify client for the Instagram Skills project.

Wraps public, no-cookie Apify actors for Instagram:
- `apify~instagram-post-scraper`:
    Fetch post caption, media URLs, video play count, likes, comments, and carousel slides by post/reel URL.
- `apify~instagram-comment-scraper`:
    Fetch comments and reply threads on any post or reel.
- `apify~instagram-profile-scraper`:
    Fetch profile bio, external link, follower metrics, and recent post history.

Auth: APIFY_TOKEN env var, sent in Authorization: Bearer header.
Caching: In-process LRU (256 entries, 6h TTL).
"""
from __future__ import annotations
import json
import os
import random
import time
from collections import OrderedDict
from typing import Any, Optional

import requests

from ._env import load_env


class ApifyError(RuntimeError):
    pass


RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}
CACHE_MAX_ENTRIES = 256
CACHE_TTL_SECONDS = 6 * 60 * 60


def _retry(attempts: int = 3, base_delay: float = 0.6):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except ApifyError as e:
                    msg = str(e)
                    retryable = any(f"HTTP {s}" in msg for s in RETRYABLE_STATUSES)
                    if not retryable or attempt == attempts - 1:
                        raise
                    last_exc = e
                except (requests.ConnectionError, requests.Timeout) as e:
                    if attempt == attempts - 1:
                        raise
                    last_exc = e
                time.sleep(base_delay * (2 ** attempt) + random.uniform(0, 0.25))
            if last_exc:
                raise last_exc

        return wrapper

    return decorator


class ApifyClient:
    BASE_URL = "https://api.apify.com/v2"

    POST_ACTOR = "apify~instagram-post-scraper"
    COMMENTS_ACTOR = "apify~instagram-comment-scraper"
    PROFILE_ACTOR = "apify~instagram-profile-scraper"

    def __init__(self, token: Optional[str] = None, timeout: float = 180.0):
        load_env()
        self.token = token or os.getenv("APIFY_TOKEN")

        if not self.token:
            raise ApifyError("APIFY_TOKEN not set. Export it or pass token= explicitly.")
        self.timeout = timeout
        self._session = requests.Session()
        self._cache: OrderedDict[str, tuple[float, Any]] = OrderedDict()

    def fetch_post(self, post_url: str, *, force_refresh: bool = False) -> dict[str, Any]:
        """Fetch post / reel details by URL."""
        items = self._run_sync(
            self.POST_ACTOR,
            {"directUrls": [post_url], "resultsLimit": 1},
            force_refresh=force_refresh,
        )
        if not items:
            raise ApifyError(f"no post returned for {post_url}")
        return self._normalize_post(items[0])

    def fetch_comments(
        self, post_url: str, *, max_items: int = 30, force_refresh: bool = False
    ) -> list[dict[str, Any]]:
        """Fetch comments on an Instagram post or reel."""
        items = self._run_sync(
            self.COMMENTS_ACTOR,
            {"directUrls": [post_url], "resultsLimit": max_items},
            force_refresh=force_refresh,
        )
        return [it for it in items if isinstance(it, dict)]

    def fetch_profile(
        self, username: str, *, force_refresh: bool = False
    ) -> dict[str, Any]:
        """Fetch profile metadata and recent posts."""
        clean_user = username.strip().lstrip("@")
        items = self._run_sync(
            self.PROFILE_ACTOR,
            {"usernames": [clean_user]},
            force_refresh=force_refresh,
        )
        if not items:
            raise ApifyError(f"no profile found for @{clean_user}")
        return items[0]

    @staticmethod
    def _normalize_post(raw: dict[str, Any]) -> dict[str, Any]:
        return {
            "caption": raw.get("caption"),
            "shortcode": raw.get("shortCode"),
            "url": raw.get("url"),
            "type": raw.get("type"),  # "Video" (Reel), "Image", "Sidecar" (Carousel)
            "likesCount": raw.get("likesCount"),
            "commentsCount": raw.get("commentsCount"),
            "videoPlayCount": raw.get("videoPlayCount") or raw.get("videoViewCount"),
            "timestamp": raw.get("timestamp"),
            "ownerUsername": raw.get("ownerUsername"),
            "images": raw.get("images", []),
            "videoUrl": raw.get("videoUrl"),
            "childPosts": raw.get("childPosts", []),
            "_raw": raw,
        }

    @staticmethod
    def _cache_key(actor_id: str, payload: dict[str, Any]) -> str:
        return f"{actor_id}::{json.dumps(payload, sort_keys=True, default=str)}"

    def _cache_get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.time() - ts > CACHE_TTL_SECONDS:
            del self._cache[key]
            return None
        self._cache.move_to_end(key)
        return value

    def _cache_put(self, key: str, value: Any) -> None:
        self._cache[key] = (time.time(), value)
        self._cache.move_to_end(key)
        while len(self._cache) > CACHE_MAX_ENTRIES:
            self._cache.popitem(last=False)

    def _run_sync(
        self, actor_id: str, payload: dict[str, Any], *, force_refresh: bool = False
    ) -> list[dict[str, Any]]:
        key = self._cache_key(actor_id, payload)
        if not force_refresh:
            cached = self._cache_get(key)
            if cached is not None:
                return cached
        data = self._do_request(actor_id, payload)
        result = data if isinstance(data, list) else []
        self._cache_put(key, result)
        return result

    @_retry()
    def _do_request(self, actor_id: str, payload: dict[str, Any]) -> Any:
        url = f"{self.BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"
        r = self._session.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=self.timeout,
        )
        if r.status_code >= 400:
            try:
                body = r.json()
            except Exception:
                body = {"error": r.text[:500]}
            raise ApifyError(f"HTTP {r.status_code}: {body}")
        data = r.json()
        if isinstance(data, dict) and "error" in data:
            raise ApifyError(f"actor failed: {data['error']}")
        return data
