"""抖音 detail 浏览器业务。

本模块只负责 detail 接口的业务参数、响应解析和数据处理；浏览器启动、桥接脚本
执行及通用请求捕获由 ``browser_request_capture`` 提供。
"""

from __future__ import annotations

from typing import Any

from _platform.douyin import douyin_data_handler as _douyin_data_handler
from utils.logger import logger

from .browser_request_capture import capture_browser_request as _capture_browser_request


__all__ = [
    "fetch_detail_with_browser",
    "handle_detail_with_browser",
]


_DETAIL_PATH = "/aweme/v1/web/aweme/detail/"


async def _capture_detail(
    aweme_id: str,
    *,
    browser_aweme_id: str | None = None,
) -> dict[str, Any]:
    target_aweme_id = str(aweme_id)
    source_aweme_id = str(browser_aweme_id or target_aweme_id)
    return await _capture_browser_request(
        f"https://www.douyin.com/video/{source_aweme_id}",
        _DETAIL_PATH,
        query_replacements={"aweme_id": target_aweme_id}
        if source_aweme_id != target_aweme_id
        else None,
        response_field="aweme_detail",
    )


async def fetch_detail_with_browser(
    aweme_id: str,
    *,
    browser_aweme_id: str | None = None,
) -> dict[str, Any]:
    """打开源 detail 页面，在 BDM 签名前替换目标 aweme_id 并返回浏览器响应。"""

    target_aweme_id = str(aweme_id)
    source_aweme_id = str(browser_aweme_id or target_aweme_id)
    result = await _capture_detail(
        target_aweme_id,
        browser_aweme_id=source_aweme_id,
    )
    signature = result.get("signature") or {}
    logger.info(
        "Douyin browser detail response aweme_id=%s source_aweme_id=%s status=%s content_type=%s body_length=%s a_bogus_length=%s sec_sdk=%s",
        target_aweme_id,
        source_aweme_id,
        result.get("status"),
        result.get("contentType", ""),
        result.get("bodyLength", 0),
        signature.get("aBogusLength", 0),
        signature.get("hasSecSdkSignature", False),
    )
    return result


async def handle_detail_with_browser(
    aweme_id: str,
    *,
    browser_aweme_id: str | None = None,
) -> None:
    """抓取 detail 响应并交给现有数据处理器。"""

    result = await fetch_detail_with_browser(
        aweme_id,
        browser_aweme_id=browser_aweme_id,
    )
    payload = result.get("payload") or {}
    detail = payload.get("aweme_detail")
    if not isinstance(detail, dict) or not detail:
        raise RuntimeError("Douyin browser detail response does not contain aweme_detail")
    headers = dict(result.get("requestHeaders") or {})
    await _douyin_data_handler(detail, headers)
