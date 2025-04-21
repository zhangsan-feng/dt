
from fastapi import Request
from entity.config_enetity import config_query_, config_edit_


async def config_edit(request: Request):
    obj = await request.json()
    config_edit_(obj)
    return {
        "code": 200,
        "data": "success",
        "msg": ""
    }


async def config_query():
    pass

    return {
        "code": 200,
        "data": config_query_(),
        "msg": ""
    }
