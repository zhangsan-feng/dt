from application.entity.download_record_entity import record_query, record_delete, record_clean, record_search
from fastapi import Request

async def record_query_api(request:Request):
    page = request.query_params.get("page")
    page = int(page) if page else 1
    return await record_query(page)

async def record_delete_api(request:Request):
    json_body = await request.json()
    id = json_body["id"]
    return await record_delete(id)

async def record_clean_api():
    await record_clean()

async def record_search_api(request:Request):
    json_body = await request.json()
    key_words = json_body["key_words"]
    return await record_search(key_words)