import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import api_router
from config import Config
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Range"]
)
config = Config()
app.mount(
    "/download",
    StaticFiles(directory=config.save_path, check_dir=False),
    name="download"
)
app.include_router(api_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run('main:app', host=config.host, port=config.port, reload=True)

"""
https://github.com/wbt5/real-url
https://github.com/ihmily/DouyinLiveRecorder
https://github.com/hr3lxphr6j/bililive-go
https://github.com/putyy/res-downloader
"""