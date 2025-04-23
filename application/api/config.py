
from fastapi import Request
from application.entity.config_enetity import config_query_, config_edit_


async def config_edit_api(request: Request):
    obj = await request.json()
    config_edit_(obj)
    return {
        "code": 200,
        "data": "success",
        "msg": ""
    }


async def config_query_api():
    pass

    return {
        "code": 200,
        "data": config_query_(),
        "msg": ""
    }
