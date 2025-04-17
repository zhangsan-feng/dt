from fastapi import Request
import os
from entity.config_enetity import config



async def preview(request: Request):
    page = request.query_params.get("page")
    page = int(page) if page else 0

    file_list = []
    for root, dirs, files in os.walk(config.save_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = "http://127.0.0.1:8000" + file_path.replace("\\", "/")[1:]
            # file_path = "http://127.0.0.1:8000/api/v1" + file_path.replace("\\", "/")[1:]
            file_list.append(file_path)
    cursor = 50
    return {
        "code":200,
        "data":file_list[page * cursor:page * cursor + cursor],
        "msg":"",
    }