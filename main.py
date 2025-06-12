
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from application.entity.config_entity import ConfigEntityObject
from application.api.config_api import router as config_api_router
from application.api.preview_api import router as preview_api_router
from application.api.link_analysis_api import router as link_analysis_router
from application.api.process_api import router as process_api_router
from application.api.record_api import router as record_api_router

api_router = APIRouter()
api_router.include_router(config_api_router)
api_router.include_router(link_analysis_router)
api_router.include_router(preview_api_router)
api_router.include_router(process_api_router)
api_router.include_router(record_api_router)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Range"]
)
config = ConfigEntityObject()

app.mount(
    "/download",
    StaticFiles(directory=config.save_path, check_dir=False),
    name="download"
)
app.include_router(api_router, prefix="/api")


if __name__ == '__main__':

    uvicorn.run('main:app', host=config.host, port=config.port)

"""

https://github.com/iuroc/bilidown
https://github.com/wbt5/real-url
https://github.com/ihmily/DouyinLiveRecorder
https://github.com/hr3lxphr6j/bililive-go
https://github.com/putyy/res-downloader
https://github.com/ihmily/StreamCap
"""