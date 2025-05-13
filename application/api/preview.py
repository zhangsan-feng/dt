import json

from fastapi import Request
import os
from config import Config


async def preview_api(request: Request):
    page = request.query_params.get("page")
    page = int(page) if page else 1
    config = Config()
    file_list = []
    for root, dirs, files in os.walk(config.save_path):
        for file in files:

            if file.endswith(".wav") or file.endswith(".mp3"):
                continue
            file_path = os.path.join(root, file)
            relative_path = config.resource_path + file_path.replace(config.save_path, "").replace("\\", "/")
            file_list.append(relative_path)
    cursor = 50
    page = page - 1
    return {
        "code":200,
        "data":file_list[page * cursor:page * cursor + cursor],
        "msg":"",
    }


