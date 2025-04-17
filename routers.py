from fastapi import Request
from api.config import config_edit, config_query
from api.download_task import download_task_query,download_task_del, download_task_add
from api.preview import preview
from api.link_analysis import link_analysis
from api.download_batch import download_batch_adapter

from fastapi import APIRouter
api_router = APIRouter()


@api_router.post("/config_edit")
async def config_edit_api(request: Request):
    return await config_edit(request)

@api_router.get("/config_query")
async def config_query_api():
    return await config_query()

@api_router.get("/task_query")
async def task_query_api():
    return await download_task_query()

@api_router.post("/task_del")
async def task_del_api(request: Request):
    return await download_task_del(request)

@api_router.post("/task_add")
async def task_add_api(request: Request):
    return await download_task_add(request)

@api_router.get("/preview")
async def preview_api(request: Request):
    return await preview(request)

@api_router.post("/link_analysis")
async def link_analysis_api(request: Request):
    return await link_analysis(request)

@api_router.post("/download_batch")
async def download_batch_api(request: Request):
    return await download_batch_adapter(request)
