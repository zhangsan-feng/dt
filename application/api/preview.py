from fastapi import Request
import os
from config import Config


async def preview_api(request: Request):
    page = request.query_params.get("page")
    page = int(page) if page else 0
    config = Config()
    file_list = []
    for root, dirs, files in os.walk(config.save_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = config.resource_path + file_path.replace(config.save_path, "").replace("\\", "/")
            file_list.append(file_path)
    cursor = 50
    return {
        "code":200,
        "data":file_list[page * cursor:page * cursor + cursor],
        "msg":"",
    }