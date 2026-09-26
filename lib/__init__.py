"""Shared helpers for Instagram Skills.

Public surface exported for all skills. Lazy-loads HTTP clients so manual tier
operates with zero dependencies.
"""
from ._env import load_env
from .url_parser import parse_instagram_url
from .approval import render_approval_card

load_env()

from .backend_selector import (
    active_backend,
    image_backend,
    manual_mode_message,
    publish,
    unpublish,
    fetch_post,
    fetch_comments,
    illustrate,
    illustrate_carousel,
    quote_card,
)

_LAZY_CLIENTS = {
    "PubloraClient": "publora_client",
    "PubloraError": "publora_client",
    "ApifyClient": "apify_client",
    "ApifyError": "apify_client",
    "PixfaroClient": "pixfaro_client",
    "PixfaroError": "pixfaro_client",
}


def __getattr__(name: str):
    module = _LAZY_CLIENTS.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    value = getattr(import_module(f".{module}", __name__), name)
    globals()[name] = value
    return value


__all__ = [
    "parse_instagram_url",
    "render_approval_card",
    "active_backend",
    "image_backend",
    "manual_mode_message",
    "publish",
    "unpublish",
    "fetch_post",
    "fetch_comments",
    "illustrate",
    "illustrate_carousel",
    "quote_card",
    "PubloraClient",
    "PubloraError",
    "ApifyClient",
    "ApifyError",
    "PixfaroClient",
    "PixfaroError",
]
