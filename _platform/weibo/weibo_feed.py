from utils import generate_random_string
from utils.http_utls import HttpRequest


async def weibo_user_feed(link, user_agent, cookie):
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

    uid = link.split("?")[0].replace("https://weibo.com/u/", "")
    page = 1
    while page > 0:

        params = {
            "uid": uid,
            "page": page,
            "feature": "0",
        }
        url = "https://weibo.com/ajax/statuses/mymblog"
        response = await HttpRequest(url, headers).httpx_get(params)