import asyncio

from _platform.bilibili.sign.w_rid import gen_w_rid_params
from utils.http_utls import HttpRequest


async def bilibili_collect(link, user_agent, cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com/',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bilibili.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent':user_agent,
        'cookie': cookie,
    }

    media_id = link.split("?")[1].split("&")[0].split("=")[1]

    params = {
        "media_id": media_id,
        "pn": 1,
        "ps" : "20",
        "keyword":"",
        "order": "mtime",
        "type" :0,
        "tid" : 0,
        "platform":"web",
    }
    params = gen_w_rid_params(params)
    url = "https://api.bilibili.com/x/v3/fav/resource/list"
    response = await HttpRequest(url, headers).httpx_get(params)
    print(response.text)


if __name__ == '__main__':
    asyncio.run(
        bilibili_collect(
            "https://space.bilibili.com/32306820/favlist?fid=3127242420&q=111",
            "",
            "",
        )
    )

