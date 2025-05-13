
from utils.http_utls import HttpRequest

async def hongshu_post(link, cookie, user_agent):
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/user_posted"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': cookie,
        'origin': 'https://www.xiaohongshu.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
        'x-b3-traceid': '',
        'x-s': '=',
        'x-s-common': '',
        'x-t': '',
        'x-xray-traceid': '',
    }
    params = {
        "num":30,
        "cursor":"",
        "user_id":'user_id',
        "image_formats":"jpg,webp,avif",
        "xsec_token":"",
        "xsec_source":""
    }
    response = await HttpRequest(url, headers).httpx_get(params=params)