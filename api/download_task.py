from datetime import datetime
from sqlmodel import Session, select
from fastapi import Request
from entity.download_task_entity import task_delete, task_update, task_query, task_add


async def download_task_query():
    data = await task_query()
    return {"code": 200, "data": data, "msg": ""}


async def download_task_del(request: Request):
    json_body = await request.json()
    id = json_body["id"]
    await task_delete(id)
    return {"code": 200, "data": "success", "msg": ""}


async def download_task_update(id, user_id, status, total, platform):
    await task_update(id, status, total, platform)
    return {"code": 200, "data": "success", "msg": ""}

async def download_task_add(request: Request):
    json_body = await request.json()
    link = json_body["link"]
    await task_add(link)
    return {"code": 200, "data": "success", "msg": ""}

async def task_start():
    pass
