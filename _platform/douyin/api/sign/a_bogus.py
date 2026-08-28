import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Mapping
from urllib.parse import quote, urlencode

from utils.logger import logger


_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_SIGNER = (
    _PROJECT_ROOT
    / "Spider_Dy_comment2"
    / "reverse_a_bogus"
    / "pure_a_bogus.js"
)


def _resolve_signer() -> Path:
    configured = os.getenv("DOUYIN_ABOGUS_SIGNER")
    signer = Path(configured).expanduser() if configured else _DEFAULT_SIGNER
    if not signer.is_file():
        raise FileNotFoundError(
            f"Douyin a_bogus signer not found: {signer}. "
            "Set DOUYIN_ABOGUS_SIGNER to the pure_a_bogus.js path."
        )
    return signer


def _resolve_node() -> str:
    configured = os.getenv("DOUYIN_NODE_BINARY")
    node = configured or shutil.which("node")
    if not node:
        raise FileNotFoundError(
            "Node.js is required for the Douyin pure a_bogus signer. "
            "Set DOUYIN_NODE_BINARY to the node executable path."
        )
    return node


def _build_unsigned_url(endpoint: str, params: Mapping[str, object]) -> str:
    clean_params = {
        key: value
        for key, value in params.items()
        if value is not None and key not in {"a_bogus", "timestamp", "x-secsdk-web-signature"}
    }
    query = urlencode(clean_params, quote_via=quote)
    return f"{endpoint}?{query}" if query else endpoint


def generate_a_bogus(
    endpoint: str,
    params: Mapping[str, object],
    user_agent: str,
    screen: Mapping[str, object] | None = None,
) -> tuple[str, str]:
    """Generate a detail request URL with the current pure a_bogus algorithm."""

    signer = _resolve_signer()
    node = _resolve_node()
    unsigned_url = _build_unsigned_url(endpoint, params)
    command = [node, str(signer), unsigned_url, f"--ua={user_agent}"]
    if screen:
        command.append(f"--screen-json={json.dumps(dict(screen), separators=(',', ':'))}")
    try:
        process = subprocess.run(
            command,
            cwd=str(signer.parent),
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except subprocess.TimeoutExpired as exc:
        logger.error("Douyin a_bogus signer timed out endpoint=%s", endpoint)
        raise RuntimeError("Douyin a_bogus signer timed out") from exc
    if process.returncode != 0:
        logger.error(
            "Douyin a_bogus signer failed endpoint=%s returncode=%s stderr_length=%s",
            endpoint,
            process.returncode,
            len(process.stderr),
        )
        raise RuntimeError("Douyin a_bogus signer failed")

    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        logger.error(
            "Douyin a_bogus signer returned invalid JSON endpoint=%s output_length=%s",
            endpoint,
            len(process.stdout),
        )
        raise RuntimeError("Douyin a_bogus signer returned invalid JSON") from exc

    signed_url = result.get("signedUrl")
    a_bogus = result.get("aBogus")
    if not isinstance(signed_url, str) or not signed_url:
        raise RuntimeError("Douyin a_bogus signer returned no signed URL")
    if not isinstance(a_bogus, str) or not a_bogus:
        raise RuntimeError("Douyin a_bogus signer returned no a_bogus")

    logger.info(
        "Douyin a_bogus generated endpoint=%s params=%s length=%s",
        endpoint,
        len(params),
        len(a_bogus),
    )
    return signed_url, a_bogus
