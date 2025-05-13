from fastapi import Request
from fastapi import APIRouter
from application.api.config_api import config_edit_api, config_query_api
from application.api.download_batch import download_batch_query_api,download_batch_del_api, download_batch_add_api, download_batch_start_api
from application.api.file_obj import file_object_stream
from application.api.preview import preview_api
from application.api.link_analysis import link_analysis_api
from application.api.process import process_status, process_kill
from application.api.record import record_query_api, record_delete_api, record_clean_api, record_search_api
from application.service.process_manager import kill_all

api_router = APIRouter()


@api_router.post("/config_edit")
async def config_edit(request: Request):
    return await config_edit_api(request)

@api_router.get("/config_query")
async def config_query():
    return await config_query_api()

@api_router.get("/download_batch_query")
async def download_batch_query(request: Request):
    return await download_batch_query_api(request)

@api_router.post("/download_batch_del")
async def download_batch_del(request: Request):
    return await download_batch_del_api(request)

@api_router.post("/download_batch_add")
async def download_batch_add(request: Request):
     return await download_batch_add_api(request)

@api_router.post("/download_batch_start")
async def download_batch_start(request: Request):
     return await download_batch_start_api(request)

@api_router.get("/preview")
async def preview(request: Request):
    return await preview_api(request)

@api_router.post("/link_analysis")
async def link_analysis(request: Request):
    return await link_analysis_api(request)

@api_router.get("/download_record_query")
async def record_query(request: Request):
    return await record_query_api(request)

@api_router.post("/download_record_delete")
async def record_delete(request: Request):
    return await record_delete_api(request)

@api_router.post("/download_record_clean")
async def record_clean():
    await record_clean_api()

@api_router.get("/download_record_search")
async def record_search(request: Request):
    return await record_search_api(request)

@api_router.get("/download_manger_query")
async def download_manger_query():
    return await process_status()

@api_router.post("/download_manger_kill")
async def download_manger_kill(request: Request):
    return await process_kill(request)

@api_router.post("/download_manger_kill_all")
async def download_manger_kill_all(request: Request):
    await kill_all()
