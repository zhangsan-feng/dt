from contextlib import suppress
from sys import platform
from types import SimpleNamespace
from typing import TYPE_CHECKING

from rookiepy import (
    arc,
    brave,
    chrome,
    chromium,
    edge,
    firefox,
    librewolf,
    opera,
    opera_gx,
    vivaldi,
)





SUPPORT_BROWSER = {

    "Chrome": (chrome, "Linux, macOS, Windows"),
}

print(chrome())