from datetime import datetime
from sqlmodel import Session, select
from fastapi import Request
from entity.download_task_entity import task_delete, task_update, task_query, task_add


async def download_task_query():
    return await task_query()


async def download_task_del(request: Request):
    json_body = await request.json()
    id = json_body["id"]
    return await task_delete(id)


async def download_task_update(id, user_id, status, total, platform):
    return await task_update(id, status, total, platform)


async def download_task_add(request: Request):
    json_body = await request.json()
    link = json_body["link"]
    return await task_add(link)

async def task_start():
    pass
