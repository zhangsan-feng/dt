import asyncio
from _platform.bilibili.sign.w_rid import gen_w_rid_params
from utils.http_utls import HttpRequest

async def bilibili_post(link, user_agent, cookie):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://space.bilibili.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://space.bilibili.com/2131609593',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
        'cookie': cookie,
    }

    mid = link.split("?")[0].replace("https://space.bilibili.com/", "").replace("/", "")

    params = {
         "mid": mid,
         "ps": 30,
         "tid": 0,
         "pn": 1,
         "keyword": "",
         "order": "pubdate",
         "platform": "web",
         "web_location": 1550101,
         "order_avoided": "true",
         # "dm_img_list":pr.dm_img_list,
         # "dm_img_str": pr.dm_img_str,
         # "dm_cover_img_str": pr.dm_cover_img_str,
         # "dm_img_inter": pr.dm_img_inter,
    }

    params = gen_w_rid_params(params)
    url = "https://api.bilibili.com/x/space/wbi/arc/search"
    response = await HttpRequest(url, headers).httpx_get(params)
    print(response.text)



if __name__ == '__main__':
    asyncio.run(
        bilibili_post(
            "https://space.bilibili.com/2131609593/",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "",
        )
    )