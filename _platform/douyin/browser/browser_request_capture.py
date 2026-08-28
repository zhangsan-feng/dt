"""抖音浏览器桥接的通用请求能力。

这里不包含具体接口的业务规则，只负责调用 js-reverse-mcp 的浏览器桥接脚本，
并把页面请求结果解析成 Python 数据。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from utils.browser import Browser


__all__ = ["capture_browser_request"]


_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_REQUEST_CAPTURE_BRIDGE = Path(__file__).with_name("browser_detail_capture.mjs")
_BROWSER = Browser(project_root=_PROJECT_ROOT)


def _validate_request_options(
    page_url: str,
    request_path: str,
    request_method: str,
    host_suffix: str,
    query_replacements: Mapping[str, Any] | None,
) -> None:
    if not isinstance(page_url, str) or not page_url.strip():
        raise ValueError("page_url must be a non-empty string")
    if not isinstance(request_path, str) or not request_path.startswith("/") or "?" in request_path:
        raise ValueError("request_path must be a URL pathname")
    if not isinstance(request_method, str) or not request_method.strip():
        raise ValueError("request_method must be a non-empty string")
    if not isinstance(host_suffix, str):
        raise ValueError("host_suffix must be a string")
    if query_replacements is not None and not isinstance(query_replacements, Mapping):
        raise ValueError("query_replacements must be a mapping")


def _bridge_options(
    request_path: str,
    request_method: str,
    host_suffix: str,
    query_replacements: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "request_path": request_path,
        "request_method": request_method,
        "host_suffix": host_suffix,
        "replace_query": dict(query_replacements or {}),
    }


async def capture_browser_request(
    page_url: str,
    request_path: str,
    *,
    query_replacements: Mapping[str, Any] | None = None,
    response_field: str | None = None,
    request_method: str = "GET",
    host_suffix: str = "douyin.com",
) -> dict[str, Any]:
    """打开页面并捕获匹配请求的浏览器响应。"""

    _validate_request_options(
        page_url,
        request_path,
        request_method,
        host_suffix,
        query_replacements,
    )
    options = _bridge_options(
        request_path,
        request_method,
        host_suffix,
        query_replacements,
    )
    options["response_field"] = response_field or ""
    result = await _BROWSER.run_bridge_json(
        _REQUEST_CAPTURE_BRIDGE,
        page_url,
        **options,
    )
    if not isinstance(result, dict):
        raise RuntimeError("Browser request capture returned an invalid result")
    return result
