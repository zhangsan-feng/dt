
from utils import generate_random_string
from utils.http_utls import HttpRequest





async def weibo_user_image(link, user_agent, cookie):
    url = "https://weibo.com/ajax/profile/getImageWall"
    uid = link.split("?")[0].replace("https://weibo.com/u/", "")
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'client-version': 'v2.46.33',
        'cookie': cookie,
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': link,
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'server-version': 'v2024.11.13.2',
        'user-agent': user_agent,
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': generate_random_string(24),
    }

    sinceid = 0
    while True:
        params ={
            "sinceid": sinceid,
            "uid": uid,
            "has_album":True,
        }

        response = await HttpRequest(url, headers).httpx_get(params)