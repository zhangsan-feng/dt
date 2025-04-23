from fastapi import Request
from fastapi import APIRouter

from application.api.config import config_edit_api, config_query_api
from application.api.download_task import download_task_query,download_task_del, download_task_add, task_start_api
from application.api.preview import preview_api
from application.api.link_analysis import link_analysis_api
from application.api.download_batch import download_batch_adapter
from application.api.record import record_query_api, record_delete_api

api_router = APIRouter()


@api_router.post("/config_edit")
async def config_edit(request: Request):
    return await config_edit_api(request)

@api_router.get("/config_query")
async def config_query():
    return await config_query_api()

@api_router.get("/task_query")
async def task_query():
    return await download_task_query()

@api_router.post("/task_del")
async def task_del(request: Request):
    return await download_task_del(request)

@api_router.post("/task_add")
async def task_add(request: Request):
    return await download_task_add(request)

@api_router.get("/task_start")
async def task_start():
    await task_start_api()

@api_router.get("/preview")
async def preview(request: Request):
    return await preview_api(request)

@api_router.post("/link_analysis")
async def link_analysis(request: Request):
    return await link_analysis_api(request)

@api_router.post("/download_batch")
async def download_batch(request: Request):
    return await download_batch_adapter(request)

@api_router.get("/record_query")
async def record_query():
    return await record_query_api()

@api_router.post("/record_delete")
async def record_delete(request: Request):
    return await record_delete_api(request)