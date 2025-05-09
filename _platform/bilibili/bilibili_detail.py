import datetime
from _platform.bilibili import bilibili_data_handler
from utils.http_utls import HttpRequest
from _platform.bilibili.sign.w_rid import gen_w_rid_params
import asyncio

async def bilibili_detail(bvid, user_agent, cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bilibili.com/video/BV1BmVUzQEpA/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=07a93c10e5d494e36d02dadbc6127d3d',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
        'cookie': cookie,
    }

    url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    response = await HttpRequest(url, headers=headers).httpx_get()
    response_body = response.json()
    # print(response.text)

    aid = response_body["data"]["aid"]
    cid = response_body["data"]["cid"]
    author = response_body["data"]["owner"]["name"]
    author_id = response_body["data"]["owner"]["mid"]
    title = response_body["data"]["title"]
    # print(aid, bvid, cid)

    params = {
        "qn":"32",
        "fnver":"0",
        "fnval":"4048",
        "fourk":"1",
        "voice_balance":"1",
        "gaia_source":"pre-load",
        "isGaiaAvoided":"true",
        "avid":aid,
        "bvid":bvid,
        "cid":cid,
        "web_location":"1315873",
        # "dm_img_list":"",
        # "dm_img_str":"",
        # "dm_cover_img_str":"",
        # "dm_img_inter":"",
        "w_rid":"",
        "wts":""
    }
    url = "https://api.bilibili.com/x/player/wbi/playurl"
    params = gen_w_rid_params(params)
    response = await HttpRequest(url, headers=headers).httpx_get(params)
    dash = response.json()['data']['dash']
    # print(response.text)

    await bilibili_data_handler(dash, author, title, bvid, author_id, headers)
    pass



if __name__ == '__main__':
    """
    https://www.bilibili.com/video/BV1N1421D7tX?spm_id_from=333.788.recommend_more_video.0&vd_source=07a93c10e5d494e36d02dadbc6127d3d
    
    """

    asyncio.run(
        bilibili_detail(
            "BV1N1421D7tX",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            ""
        )
    )