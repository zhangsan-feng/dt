import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import api_router
from entity.config_enetity import config_query_
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Range"]
)

app.mount(
    "/download",
    StaticFiles(directory=config_query_().save_path, check_dir=False),
    name="download"
)
app.include_router(api_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)

"""
https://github.com/wbt5/real-url
https://github.com/ihmily/DouyinLiveRecorder
https://github.com/hr3lxphr6j/bililive-go
https://github.com/putyy/res-downloader
"""