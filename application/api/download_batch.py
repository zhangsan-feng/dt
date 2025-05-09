from fastapi import Request
from application.entity.download_batch_entity import batch_query, batch_delete, batch_update, batch_add, batch_query_all
from application.service.link_analysis import link_analysis

async def download_batch_query_api(request:Request):
    page = request.query_params.get("page")
    page = int(page) if page else 1
    data = await batch_query(page)
    return {"code": 200, "data": data, "msg": ""}


async def download_batch_del_api(request: Request):
    json_body = await request.json()
    id = json_body["id"]
    await batch_delete(id)
    return {"code": 200, "data": "success", "msg": ""}


async def download_batch_update_api(id, user_id, status, total, platform):
    await batch_update(id, status, total, platform)
    return {"code": 200, "data": "success", "msg": ""}

async def download_batch_add_api(request: Request):
    json_body = await request.json()
    link = json_body["link"]
    await batch_add(link)
    return {"code": 200, "data": "success", "msg": ""}

async def download_batch_start_api(request: Request):
    user_agent = dict(request.headers)["user-agent"]
    rows = await batch_query_all()
    for column in rows:
        print(column)
        await link_analysis(column.link, user_agent)
    return {"code": 200, "data": "开始下载", "msg": ""}