
from fastapi import Request, APIRouter
from application.entity.config_entity import ConfigEntityObject

router = APIRouter()

@router.post("/config_edit")
async def config_edit_api(request: Request):
    obj = await request.json()
    ConfigEntityObject().edit(obj)
    return {
        "code": 200,
        "data": "success",
        "msg": ""
    }

@router.get("/config_query")
async def config_query_api():

    return {
        "code": 200,
        "data": ConfigEntityObject(),
        "msg": ""
    }
