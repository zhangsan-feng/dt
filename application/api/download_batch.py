from fastapi import Request
from application.entity.download_batch_entity import batch_query, batch_delete, batch_update, batch_add


async def download_batch_query():
    data = await batch_query()
    return {"code": 200, "data": data, "msg": ""}


async def download_batch_del(request: Request):
    json_body = await request.json()
    id = json_body["id"]
    await batch_delete(id)
    return {"code": 200, "data": "success", "msg": ""}


async def download_batch_update(id, user_id, status, total, platform):
    await batch_update(id, status, total, platform)
    return {"code": 200, "data": "success", "msg": ""}

async def download_batch_add(request: Request):
    json_body = await request.json()
    link = json_body["link"]
    await batch_add(link)
    return {"code": 200, "data": "success", "msg": ""}

async def batch_start_api():
    pass
