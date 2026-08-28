import asyncio
import json
from urllib.parse import parse_qs
from _platform.hongshu import hongshu_data_handler
from _platform.hongshu.sign import gen_headers_sign

from utils.http_utls import HttpRequest

async def hongshu_detail(link, user_agent, cookie):
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/feed"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.xiaohongshu.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
        'x-b3-traceid': '',
        'x-mns': 'unload',
        'x-s': '',
        'x-s-common': '',
        'x-t': '',
        'x-xray-traceid': '',
        'cookie': cookie,
    }
    source_note_id = link.split("?")[0].replace("https://www.xiaohongshu.com/explore/","").replace("https://www.xiaohongshu.com/discovery/item/", "")
    xsec_token = parse_qs(link.split("?")[1])["xsec_token"][0]
    # print(source_note_id, xsec_token)
    params = {
        'source_note_id': source_note_id,
        'image_formats': [
            'jpg',
            'webp',
            'avif',
        ],
        'extra': {
            'need_body_topic': '1',
        },
        'xsec_source': 'pc_feed',
        'xsec_token': xsec_token,
    }

    await gen_headers_sign(headers, "/api/sns/web/v1/feed" ,params)
    response = await HttpRequest(url, headers).httpx_post(data=json.dumps(params, separators=(',', ':')))
    # print(response.text)
    response_body = response.json()["data"]["items"]

    await hongshu_data_handler(response_body, headers)

if __name__ == '__main__':

    asyncio.run(
        hongshu_detail(
            "https://www.xiaohongshu.com/explore/680f39c40000000009015580?xsec_token=ABM7LSXE2Ett4PlvQ2rsdKen7-rfb38R9a0vyIaN-iByE=&xsec_source=pc_feed",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            ""
        )
    )