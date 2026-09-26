"""Thin Pixfaro client for Instagram visual asset generation.

Specialized for Instagram dimensions:
- Carousels & Feed posts: 4:5 aspect ratio (1080x1350)
- Reels & Stories: 9:16 aspect ratio (1080x1920)
- Legacy / Grid square: 1:1 aspect ratio (1080x1080)

Generates hosted image URLs and renders HTML-typeset cards with crisp typography.
Auth: PIXFARO_TOKEN env var.
"""
from __future__ import annotations
import base64
import json
import os
import random
import time
from collections import OrderedDict
from typing import Any, Optional

import requests

from ._env import load_env


class PixfaroError(RuntimeError):
    def __init__(self, message: str, status_code: Optional[int] = None, retryable: bool = False):
        super().__init__(message)
        self.status_code = status_code
        self.retryable = retryable


BASE_URL = "https://api.pixfaro.com/v1"
DEFAULT_MODEL = "nano-banana-2"
RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}
CACHE_MAX_ENTRIES = 128
CACHE_TTL_SECONDS = 6 * 60 * 60
MAX_LOGO_BYTES = 1_048_576


def _retry(attempts: int = 3, base_delay: float = 0.6):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except PixfaroError as e:
                    if not getattr(e, "retryable", False) or attempt == attempts - 1:
                        raise
                    last_exc = e
                    time.sleep(base_delay * (2 ** attempt) + random.uniform(0, 0.3))
            if last_exc:
                raise last_exc
        return wrapper
    return decorator


class PixfaroClient:
    def __init__(self, api_key: Optional[str] = None, timeout: float = 90.0):
        load_env()
        self.api_key = api_key or os.getenv("PIXFARO_TOKEN") or os.getenv("PIXFARO_API_KEY")
        if not self.api_key:
            raise PixfaroError(
                "No Pixfaro API key. Set PIXFARO_TOKEN (pf_live_...) or pass api_key."
            )
        self.timeout = timeout
        self._session = requests.Session()
        self._cache: OrderedDict[str, tuple[float, dict]] = OrderedDict()

    def _cache_get(self, key: str) -> Optional[dict]:
        hit = self._cache.get(key)
        if not hit:
            return None
        ts, val = hit
        if time.time() - ts > CACHE_TTL_SECONDS:
            self._cache.pop(key, None)
            return None
        self._cache.move_to_end(key)
        return val

    def _cache_put(self, key: str, val: dict) -> None:
        self._cache[key] = (time.time(), val)
        self._cache.move_to_end(key)
        while len(self._cache) > CACHE_MAX_ENTRIES:
            self._cache.popitem(last=False)

    @_retry()
    def generate(
        self,
        prompt: str,
        *,
        model: str = DEFAULT_MODEL,
        aspect_ratio: str = "4:5",
        resolution: str = "1K",
        overlay: Optional[dict[str, Any]] = None,
        force_refresh: bool = False,
    ) -> dict[str, Any]:
        """Generate one image (defaults to 4:5 for Instagram feed/carousel)."""
        if not prompt or not prompt.strip():
            raise PixfaroError("prompt cannot be empty")

        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }
        if overlay:
            payload["overlay"] = overlay

        key = json.dumps(payload, sort_keys=True)
        if not force_refresh:
            cached = self._cache_get(key)
            if cached is not None:
                return cached

        data = self._post("/images/generations", payload)
        self._cache_put(key, data)
        return data

    @_retry()
    def render(
        self,
        template: str,
        slots: dict[str, Any],
        *,
        size: str = "4:5",
        style: Optional[Any] = None,
        overlay: Optional[Any] = None,
        force_refresh: bool = False,
    ) -> dict[str, Any]:
        """Typeset HTML card templates (quote-card, stat-card) with crisp text."""
        payload: dict[str, Any] = {
            "template": template,
            "slots": slots,
            "size": size,
        }
        if style:
            payload["style"] = style
        if overlay:
            payload["overlay"] = overlay

        key = "render:" + json.dumps(payload, sort_keys=True)
        if not force_refresh:
            cached = self._cache_get(key)
            if cached is not None:
                return cached

        data = self._post("/renders", payload)
        self._cache_put(key, data)
        return data

    def upload_logo(self, path: str, *, name: Optional[str] = None) -> dict[str, Any]:
        """Upload brand logo to reuse across overlays."""
        with open(path, "rb") as f:
            raw = f.read()
        if len(raw) > MAX_LOGO_BYTES:
            raise PixfaroError("logo must be <= 1 MB PNG")
        payload = {"image": base64.b64encode(raw).decode("ascii")}
        if name:
            payload["name"] = name
        return self._post("/logos", payload)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        url = f"{BASE_URL}{path}"
        try:
            r = self._session.post(url, json=json_body, headers=self._headers(), timeout=self.timeout)
        except requests.RequestException as e:
            raise PixfaroError(f"request failed: {e}", retryable=True) from e
        return self._handle(r)

    @staticmethod
    def _handle(r: requests.Response) -> dict[str, Any]:
        if r.status_code >= 400:
            detail = r.text[:300]
            try:
                detail = json.dumps(r.json())
            except Exception:
                pass
            raise PixfaroError(
                f"HTTP {r.status_code}: {detail}",
                status_code=r.status_code,
                retryable=r.status_code in RETRYABLE_STATUSES,
            )
        return r.json()
