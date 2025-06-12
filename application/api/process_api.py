from application.service.process_manager import query, kill
from fastapi import Request, APIRouter

router = APIRouter()

@router.get("/download_manger_query")
async def process_status():
    return await query()


@router.post("/download_manger_kill")
async def process_kill(request:Request):
    json_body = await request.json()
    uuid = json_body["uuid"]
    return await kill(uuid)