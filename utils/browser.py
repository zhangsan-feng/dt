"""通用浏览器对象。

这个模块负责两类浏览器操作：

* ``browser_call_js``：打开页面后，在浏览器页面上下文执行 JS 函数；
* ``browser_request_listener``：打开页面并监听指定响应接口。

具体的 Patchright/Chrome 操作放在同目录的 Node.js 桥接脚本中，Python 只负责
传参、等待子进程和解析结构化结果。
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from utils.logger import logger


__all__ = ["BrowserObject", "Browser", "BrowserRequest", "BrowserResponse"]


@dataclass(slots=True)
class BrowserRequest:
    """浏览器主请求的可读数据。"""

    url: str = ""
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None


@dataclass(slots=True)
class BrowserResponse:
    """浏览器主响应的可读数据。"""

    url: str = ""
    status_code: int | None = None
    status_text: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None
    body_encoding: str = "utf8"


class BrowserObject:
    _DEFAULT_TIMEOUT = 75.0

    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
        node_binary: str | None = None,
        timeout: float | None = None,
        headless: bool | None = None,
    ) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[1]
        self.node_binary = node_binary
        self.timeout = timeout
        self.headless = headless
        self.request: BrowserRequest | None = None
        self.response: BrowserResponse | None = None

    def _resolve_node(self) -> str:
        node = (
            self.node_binary
            or os.getenv("BROWSER_NODE_BINARY")
            or os.getenv("DOUYIN_NODE_BINARY")
            or shutil.which("node")
        )
        if not node:
            raise FileNotFoundError(
                "Node.js is required for the browser bridge. "
                "Set DOUYIN_NODE_BINARY to the node executable path."
            )
        return node

    def _resolve_timeout(self) -> float:
        if self.timeout is not None:
            return self.timeout
        timeout = os.getenv("BROWSER_TIMEOUT", os.getenv("DOUYIN_BROWSER_TIMEOUT"))
        return float(timeout) if timeout else self._DEFAULT_TIMEOUT

    def _resolve_headless(self) -> bool:
        if self.headless is not None:
            return self.headless
        return os.getenv(
            "BROWSER_HEADLESS",
            os.getenv("DOUYIN_BROWSER_HEADLESS", "false"),
        ).lower() == "true"

    def _build_command(self, script: Path, args: Sequence[str]) -> list[str]:
        command = [self._resolve_node(), str(script), *(str(arg) for arg in args)]
        if self._resolve_headless():
            command.append("--headless=true")
        return command

    @staticmethod
    def _build_environment(environment: Mapping[str, str] | None) -> dict[str, str]:
        process_environment = os.environ.copy()
        if environment:
            process_environment.update({key: str(value) for key, value in environment.items()})
        return process_environment

    @staticmethod
    def _build_extra_args(args: Sequence[Any], options: Mapping[str, Any]) -> tuple[str, ...]:
        """将扩展参数转换为桥接脚本可识别的命令行参数。"""

        if "environment" in options:
            raise TypeError("browser request methods use the browser profile cookies; environment is unsupported")

        extra = [str(arg) for arg in args]
        for name, value in options.items():
            if not isinstance(name, str) or not name:
                raise TypeError("browser request option names must be non-empty strings")
            if value is None:
                continue
            if isinstance(value, bool):
                value = str(value).lower()
            elif isinstance(value, (Mapping, list, tuple)):
                value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            extra.append(f"--{name.replace('_', '-')}={value}")
        return tuple(extra)

    async def _run_process(
        self,
        command: Sequence[str],
        environment: Mapping[str, str],
        script: Path,
    ) -> str:
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(self.project_root),
            env=environment,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self._resolve_timeout(),
            )
        except asyncio.TimeoutError as exc:
            process.kill()
            await process.communicate()
            logger.error("Browser bridge timed out script=%s", script.name)
            raise TimeoutError(f"Browser bridge timed out: {script.name}") from exc

        decoded_stdout = stdout.decode("utf-8", errors="replace")
        decoded_stderr = stderr.decode("utf-8", errors="replace")
        if process.returncode != 0:
            logger.error(
                "Browser bridge failed script=%s returncode=%s stdout_length=%s stderr_length=%s",
                script.name,
                process.returncode,
                len(decoded_stdout),
                len(decoded_stderr),
            )
            raise RuntimeError(f"Browser bridge failed: {script.name}")
        return decoded_stdout

    @staticmethod
    def _decode_json(stdout: str, script_path: Path) -> Any:
        output = stdout.strip()
        if not output:
            raise RuntimeError(f"Browser bridge returned empty output: {script_path}")

        try:
            return json.loads(output)
        except json.JSONDecodeError:
            # 允许桥接脚本在最终 JSON 前输出普通日志，取最后一行 JSON。
            for line in reversed(output.splitlines()):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        raise RuntimeError(f"Browser bridge returned invalid JSON: {script_path}")

    async def browser_call_js(
        self,
        url: str,
        script_path: str | Path,
        args: Sequence[Any] = (),
        *,
        environment: Mapping[str, str] | None = None,
    ) -> Any:
        """在浏览器页面上下文执行 JS 函数并返回其 JSON 结果。

        ``script_path`` 文件需要是一个 JS 函数表达式，例如：

        ``async ({selector}) => document.querySelector(selector)?.textContent``
        """

        if not isinstance(url, str) or not url.strip():
            raise ValueError("browser_call_js requires a non-empty URL")

        script = Path(script_path).resolve()
        if not script.is_file():
            raise FileNotFoundError(f"Browser page script not found: {script}")

        bridge = Path(__file__).with_name("browser_call_js.mjs")
        stdout = await self._run_process(
            self._build_command(
                bridge,
                (
                    url,
                    str(script),
                    f"--args-json={json.dumps(list(args), ensure_ascii=False, separators=(',', ':'))}",
                    f"--timeout-ms={int(self._resolve_timeout() * 1000)}",
                ),
            ),
            self._build_environment(environment),
            bridge,
        )
        return self._decode_json(stdout, bridge)

    async def browser_request_listener(
        self,
        url: str,
        response_url: str,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """打开页面并返回 URL 匹配的浏览器响应。

        ``args`` 和 ``kwargs`` 会作为额外命令行参数传给监听桥接脚本；Cookie
        直接来自持久化浏览器配置，不通过 Python 环境变量传递。
        """

        if not isinstance(url, str) or not url.strip():
            raise ValueError("browser_request_listener requires a non-empty URL")
        if not isinstance(response_url, str) or not response_url.strip():
            raise ValueError("browser_request_listener requires a response URL pattern")

        self.request = None
        self.response = None
        bridge = Path(__file__).with_name("browser_request_listener.mjs")
        extra_args = self._build_extra_args(args, kwargs)
        stdout = await self._run_process(
            self._build_command(
                bridge,
                (
                    url,
                    response_url,
                    *extra_args,
                    f"--timeout-ms={int(self._resolve_timeout() * 1000)}",
                ),
            ),
            self._build_environment(None),
            bridge,
        )
        result = self._decode_json(stdout, bridge)
        self._record_browser_exchange(result)
        return result

    async def run_bridge_json(
        self,
        bridge_path: str | Path,
        url: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """运行一个浏览器桥接脚本并解析其 JSON 输出。"""

        if not isinstance(url, str) or not url.strip():
            raise ValueError("run_bridge_json requires a non-empty URL")

        bridge = Path(bridge_path).resolve()
        if not bridge.is_file():
            raise FileNotFoundError(f"Browser bridge not found: {bridge}")

        extra_args = self._build_extra_args(args, kwargs)
        stdout = await self._run_process(
            self._build_command(
                bridge,
                (
                    url,
                    *extra_args,
                    f"--timeout-ms={int(self._resolve_timeout() * 1000)}",
                ),
            ),
            self._build_environment(None),
            bridge,
        )
        return self._decode_json(stdout, bridge)

    @staticmethod
    def _headers(value: Any) -> dict[str, str]:
        if not isinstance(value, Mapping):
            return {}
        return {str(name): str(header) for name, header in value.items()}

    def _record_browser_exchange(self, result: Any) -> None:
        if not isinstance(result, Mapping):
            raise RuntimeError("Browser request result must be an object")

        request = result.get("request")
        response = result.get("response")
        if not isinstance(request, Mapping) or not isinstance(response, Mapping):
            raise RuntimeError("Browser request result must contain request and response objects")

        self.request = BrowserRequest(
            url=str(request.get("url") or ""),
            method=str(request.get("method") or "GET"),
            headers=self._headers(request.get("headers")),
            body=request.get("body"),
        )
        self.response = BrowserResponse(
            url=str(response.get("url") or ""),
            status_code=response.get("statusCode"),
            status_text=str(response.get("statusText") or ""),
            headers=self._headers(response.get("headers")),
            body=response.get("body"),
            body_encoding=str(response.get("bodyEncoding") or "utf8"),
        )

    async def browser_request(
        self,
        url: str,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """通过浏览器访问 URL，并记录主请求和主响应对象。"""

        if not isinstance(url, str) or not url.strip():
            raise ValueError("browser_request requires a non-empty URL")

        self.request = None
        self.response = None
        bridge = Path(__file__).with_name("browser_request.mjs")
        extra_args = self._build_extra_args(args, kwargs)
        stdout = await self._run_process(
            self._build_command(
                bridge,
                (
                    url,
                    *extra_args,
                    f"--timeout-ms={int(self._resolve_timeout() * 1000)}",
                ),
            ),
            self._build_environment(None),
            bridge,
        )
        result = self._decode_json(stdout, bridge)
        self._record_browser_exchange(result)
        return result


# 兼容尚未迁移的旧导入：from utils.browser import Browser
Browser = BrowserObject
