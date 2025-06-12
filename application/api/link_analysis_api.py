

from fastapi import Request, APIRouter
from utils import match_url
from utils.logger import logger
from application.service.link_analysis import link_analysis

router = APIRouter()

@router.post("/link_analysis")
async def link_analysis_api(request: Request):
    json_body = await request.json()
    logger.info(json_body)

    link = json_body["link"] if "link" in json_body else None
    file_path = json_body["file_path"] if "file_path" in json_body else None

    link = match_url(link)
    logger.info(link, file_path)
    user_agent = dict(request.headers)["user-agent"]

    if link:
        await link_analysis(link, user_agent)
    if file_path:
        with open(file_path, "r+") as f:
            content = f.readlines()
        for line in content:
            await link_analysis(match_url(line), user_agent)

    return {"code":200, "data":"已经加入下载队列", "msg":""}