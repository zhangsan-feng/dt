from utils import generate_random_string
from utils.http_utls import HttpRequest

async def weibo_detail(link, user_agent, cookie):

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
        'x-xsrf-token': generate_random_string(24)
    }


    id = link.split("?")[0].split("/")
    params = {
        "id":id[-1],
        "locale":"zh-CN"
    }
    url = "https://weibo.com/ajax/statuses/show"
    response = HttpRequest(url, headers).httpx_get(params)


async def weibo_tv():
    pass

    # let task_name = url
    #
    # let video_id = url.split("?")[0].replace("https://weibo.com","")
    # let oid = video_id.replace("/tv/show/", "")
    # let data = {
    #     'data':'{"Component_Play_Playinfo":{"oid":"1034:5054603256070180"}}'
    # }
    #
    # let response = await HTTPPostForm("https://weibo.com/tv/api/component?page=" + video_id, data, headers)
    # console.log(response)
