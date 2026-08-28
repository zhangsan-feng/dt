"""抖音用户主页作品浏览器业务。"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from _platform.douyin import douyin_data_handler as _douyin_data_handler
from utils.logger import logger

from .browser_request_capture import capture_browser_request


__all__ = ["fetch_post_page_with_browser", "handle_post_with_browser"]


_POST_PATH = "/aweme/v1/web/aweme/post/"
_DOUYIN_HOSTS = ("douyin.com", "iesdouyin.com")


def _parse_user_url(user_url: str) -> tuple[str, str]:
    if not isinstance(user_url, str) or not user_url.strip():
        raise ValueError("user_url must be a non-empty string")

    normalized_url = user_url.strip()
    parsed = urlsplit(normalized_url)
    hostname = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"} or not any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in _DOUYIN_HOSTS
    ):
        raise ValueError("user_url must be a Douyin user URL")

    segments = [segment for segment in parsed.path.split("/") if segment]
    if len(segments) >= 2 and segments[0] == "user":
        sec_user_id = segments[1]
    elif len(segments) >= 3 and segments[:2] == ["share", "user"]:
        sec_user_id = segments[2]
    else:
        raise ValueError("user_url must contain /user/{sec_user_id}")
    if not sec_user_id or sec_user_id == "self":
        raise ValueError("user_url must contain a concrete sec_user_id")
    return normalized_url, sec_user_id


def _post_query_replacements(
    sec_user_id: str,
    max_cursor: int | str | None,
) -> dict[str, str]:
    replacements = {"sec_user_id": sec_user_id}
    if max_cursor is not None:
        replacements["max_cursor"] = str(max_cursor)
    return replacements


def _extract_post_items(result: dict[str, Any]) -> list[dict[str, Any]]:
    payload = result.get("payload") or {}
    items = payload.get("aweme_list")
    if not isinstance(items, list):
        raise RuntimeError("Douyin browser post response does not contain aweme_list")
    return [item for item in items if isinstance(item, dict)]


async def fetch_post_page_with_browser(
    user_url: str,
    *,
    max_cursor: int | str | None = None,
) -> dict[str, Any]:
    """打开用户主页并捕获指定 max_cursor 的作品列表响应。"""

    page_url, sec_user_id = _parse_user_url(user_url)
    result = await capture_browser_request(
        page_url,
        _POST_PATH,
        query_replacements=_post_query_replacements(sec_user_id, max_cursor),
        response_field="aweme_list",
    )
    items = _extract_post_items(result)
    logger.info(
        "Douyin browser post response sec_user_id=%s max_cursor=%s status=%s item_count=%s body_length=%s",
        sec_user_id,
        max_cursor,
        result.get("status"),
        len(items),
        result.get("bodyLength", 0),
    )
    return result


async def handle_post_with_browser(
    user_url: str,
    *,
    max_cursor: int | str | None = None,
) -> int:
    """抓取用户主页作品并交给现有详情数据处理器。"""

    result = await fetch_post_page_with_browser(user_url, max_cursor=max_cursor)
    items = _extract_post_items(result)
    headers = dict(result.get("requestHeaders") or {})
    for item in items:
        await _douyin_data_handler(item, headers)
    logger.info(
        "Douyin browser post handled sec_user_id=%s item_count=%s",
        _parse_user_url(user_url)[1],
        len(items),
    )
    return len(items)
