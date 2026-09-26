"""Thin Publora REST client for the Instagram Skills project.

Wraps the Publora API endpoints for Instagram:
- POST   /create-post            (draft or scheduled; supports single photo, carousels, and reels)
- GET    /get-post/<id>          (status, platform delivery, media)
- DELETE /delete-post/<id>       (cancel scheduled post)
- GET    /platform-connections   (retrieves instagram-* connection IDs)
- GET    /platform-limits        (Instagram image, carousel and video limits)

Auth header: x-publora-key: sk_...
"""
from __future__ import annotations
import os
import random
import time
from typing import Any, Optional

import requests

from ._env import load_env


class PubloraError(RuntimeError):
    pass


RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}


def _retry(attempts: int = 3, base_delay: float = 0.6):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except PubloraError as e:
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


class PubloraClient:
    BASE_URL = "https://api.publora.com/api/v1"

    def __init__(self, api_key: Optional[str] = None, timeout: float = 45.0):
        load_env()
        self.api_key = api_key or os.getenv("PUBLORA_API_KEY")

        if not self.api_key:
            raise PubloraError(
                "PUBLORA_API_KEY not set. Export it or pass api_key= explicitly."
            )
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-publora-key": self.api_key,
                "Content-Type": "application/json",
            }
        )

    def list_platform_connections(self) -> list[dict[str, Any]]:
        """List channels connected to this Publora key."""
        r = self._session.get(f"{self.BASE_URL}/platform-connections", timeout=self.timeout)
        payload = self._handle(r)
        rows = payload.get("connections") or payload.get("data") or payload
        return rows if isinstance(rows, list) else []

    def resolve_instagram_platform_id(self) -> Optional[str]:
        """Auto-resolve the Instagram platformId if exactly one is connected."""
        connections = self.list_platform_connections()
        ig_channels = [
            c.get("platformId") for c in connections
            if str(c.get("platformId", "")).startswith("instagram-")
        ]
        return ig_channels[0] if len(ig_channels) == 1 else None

    def create_post(
        self,
        *,
        content: str,
        platforms: list[str],
        media_urls: Optional[list[str]] = None,
        scheduled_time: Optional[str] = None,
    ) -> dict[str, Any]:
        """Publish or schedule an Instagram Post, Carousel, or Reel.

        - `content`: Caption text (supports linebreaks, emojis, hashtags).
        - `platforms`: List of platformId strings, e.g. ["instagram-abc123XYZ"].
        - `media_urls`: Hosted URLs.
            - 1 image URL: Single photo post (4:5 or 1:1).
            - 2-10 image URLs: Swipeable carousel (4:5 recommended).
            - 1 video URL: Instagram Reel (9:16 MP4).
        - `scheduled_time`: ISO 8601 UTC string (e.g. '2026-09-28T10:00:00Z').
        """
        if not media_urls and not content:
            raise PubloraError("Instagram requires either media_urls or caption content.")

        norm_platforms = [
            p if isinstance(p, str) else (p.get("platformId") or p.get("platform"))
            for p in platforms
        ]

        payload: dict[str, Any] = {
            "content": content,
            "platforms": norm_platforms,
        }
        if media_urls:
            payload["mediaUrls"] = media_urls
        if scheduled_time:
            payload["scheduledTime"] = scheduled_time

        return self._post("/create-post", payload)

    def get_post(self, *, post_group_id: str) -> dict[str, Any]:
        """Retrieve status and metadata for a post group."""
        r = self._session.get(
            f"{self.BASE_URL}/get-post/{post_group_id}", timeout=self.timeout
        )
        return self._handle(r)

    def delete_post(self, *, post_group_id: str) -> dict[str, Any]:
        """Cancel a scheduled post or draft."""
        r = self._session.delete(
            f"{self.BASE_URL}/delete-post/{post_group_id}",
            timeout=self.timeout,
        )
        return self._handle(r)

    @_retry()
    def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        r = self._session.post(
            self.BASE_URL + path, json=json_body, timeout=self.timeout
        )
        return self._handle(r)

    @staticmethod
    def _handle(r: requests.Response) -> dict[str, Any]:
        if r.status_code >= 400:
            try:
                body = r.json()
            except Exception:
                body = {"error": r.text[:500]}
            raise PubloraError(f"HTTP {r.status_code}: {body}")
        return r.json()
