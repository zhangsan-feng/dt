import asyncio

from _platform.bilibili import bilibili_live_handler
from utils import word_analysis, gen_uid
from utils.http_utls import HttpRequest

async def bilibili_live(link, user_agent):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://live.bilibili.com/',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://live.bilibili.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent':user_agent,
    }


    room_id =  link.split("?")[0].replace("https://live.bilibili.com/","")

    params = {
        "room_id":room_id,
        "mask":"1",
        "qn":"0",
        "platform":"web",
        "protocol":"0,1",
        "format":"0,1,2",
        "codec":"0,1,2",
        "dolby":"5",
        "panorama":"1",
    }
    url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo"
    response = await HttpRequest(url, headers).httpx_get(params)
    response_body = response.json()
    # print(response_body)

    info = response_body['data']["playurl_info"]["playurl"]["stream"][0]["format"][0]["codec"][0]
    uids = response_body['data']["uid"]
    flv_stream_url = info["url_info"][0]["host"] + info["base_url"] + info["url_info"][0]["extra"]

    params = {
        "uids":uids,
        "req_biz":"video"
    }
    url = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"

    response = await HttpRequest(url, headers).httpx_get(params)
    response_body = response.json()
    # print(response_body)

    author = word_analysis(response_body['data']["by_uids"][str(uids)]["uname"])
    title = word_analysis(response_body['data']["by_uids"][str(uids)]["title"])
    headers['referer'] = flv_stream_url
    await bilibili_live_handler(author, title, flv_stream_url, headers)








if __name__ == '__main__':
    asyncio.run(
        bilibili_live(
            "",
            ""
        )
    )