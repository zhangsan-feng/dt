from utils.http_utls import HttpRequest

import asyncio

async def bilibili_detail(bvid, cid):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bilibili.com',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        # 'cookie': '',
    }
    url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid

    url = "https://api.bilibili.com/x/player/wbi/playurl"

    params = {
        "qn":"32",
        "fnver":"0",
        "fnval":"4048",
        "fourk":"1",
        "voice_balance":"1",
        "gaia_source":"pre-load",
        "isGaiaAvoided":"true",
        "avid":"889193331",
        "bvid":"BV1KP4y147PZ",
        "cid":"372195252",
        "web_location":"1315873",
        "dm_img_list":"",
        "dm_img_str":"",
        "dm_cover_img_str":"",
        "dm_img_inter":"",
        "w_rid":"12187a5a4fcd15a8f3454136bc9db5f5",
        "wts":"1745559900"
    }

    pass



if __name__ == '__main__':
    asyncio.run(
        bilibili_detail(
            "",
            ""
        )
    )