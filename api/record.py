from entity.record_entity import record_query, record_delete
from fastapi import Request

async def record_query_api_():
    return await record_query()

async def record_delete_api_(request:Request):
    json_body = await request.json()
    id = json_body["id"]
    return await record_delete(id)