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
            # 转换为相对于资源路径的路径
            relative_path = config.resource_path + file_path.replace(config.save_path, "").replace("\\", "/")
            file_list.append((relative_path, os.path.getctime(file_path)))

    file_list.sort(key=lambda x: x[1])

    sorted_file_list = [file[0] for file in file_list]
    cursor = 50
    return {
        "code":200,
        "data":sorted_file_list[page * cursor:page * cursor + cursor],
        "msg":"",
    }