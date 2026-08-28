"""项目运行配置。"""

from __future__ import annotations

import os
from pathlib import Path


_PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _directory(value: str | None, default: Path) -> str:
    path = Path(value).expanduser() if value else default
    path.mkdir(parents=True, exist_ok=True)
    return str(path.resolve()).replace("\\", "/").rstrip("/") + "/"


class Configuration:

    def __init__(self) -> None:
        self.project_path = _directory(os.getenv("DT_PROJECT_PATH"), _PROJECT_ROOT)
        self.download_path = _directory(
            os.getenv("DT_DOWNLOAD_PATH"),
            _PROJECT_ROOT / "download",
        )
        self.save_path = self.download_path

        self.douyin_path = _directory(None, Path(self.save_path) / "douyin")
        self.bilibili_path = _directory(None, Path(self.save_path) / "bilibili")
        self.hongshu_path = _directory(None, Path(self.save_path) / "hongshu")

        self.douyin_cookie = os.getenv("DOUYIN_COOKIE", "")
        self.bilibili_cookie = os.getenv("BILIBILI_COOKIE", "")
        self.hongshu_cookie = os.getenv("HONGSHU_COOKIE", "")
        self.weibo_cookie = os.getenv("WEIBO_COOKIE", "")
        self.kuaishou_cookie = os.getenv("KUAISHOU_COOKIE", "")

        self.only_download_audio = False
        self.only_download_video = False
        self.only_download_image = False

        self.download_limit_num = 300
        self.download_limit = False
        self.download_format = True
        self.download_filter = False
        self.download_delay = True
        self.download_delay_num = 1.5

    def get_cookie(self, platform: str) -> str:
        return str(getattr(self, f"{platform}_cookie", "") or "")

