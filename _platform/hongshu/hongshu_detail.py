import asyncio
import json
from urllib.parse import urlencode

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
        'x-b3-traceid': '96871b6ff1af70f8',
        'x-mns': 'unload',
        'x-s': 'XYW_eyJzaWduU3ZuIjoiNTYiLCJzaWduVHlwZSI6IngyIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6IjAzY2ZiZjUwYmY2MWZmZjhjM2MwNmFiN2IzMzczNTFhZmY0NGE2YWE3MDBmYTk0NjcwYTdkODQyMTZlMTQxMmI0ODcyOTI5OGNhYzEwZjFiYzBmNjJmMjMwODNiZWM2NDZiNDZhOGRlOTMxOTkzZjFhOWQ0N2MwNTNhNTEwNzVlZjc3MDBhZTc1NDc2OTBmM2RmNWI4YWQ4NTBmYzk4NTRmMmQ0MWUxNjcyODgwMTZhYmYwNjQ4OTRjZGQ5NGI5NjI5N2UwN2Y4MjEyYzYzODQxYmUxY2UxNDQwMWY4YjI5M2VkOGQ3Zjg3NGZhM2RjMjcxNGNhNWJiYTcxODE3YTI2M2M3YjNmMTZhOWE0ODFkNGFmNTI2ZGZlNThjZjgyM2Y3NzRlNDI4OGMyNGQ5MWNhY2I5NzQ3NmViMWU1Mzk3ZGZkOWFjNGRjZWI4MzI0NDRiMDViYTAyNTgxMWEzZTMxNzE0ZGU4MDY4YWY4MjA0MzM3MjRiYTc3YjFiZTE4ZmUyNDA3OWRkMDkyODc4MjczZjNkZTViMzU2ZWZjYzhjIn0=',
        'x-s-common': '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',
        'x-t': '1747101564577',
        'x-xray-traceid': 'cb63af1f28dfe7c53941fc12d0b078cd',
        'cookie': 'abRequestId=ebaf4b6d-bd97-51c3-a8bb-6c84965c5109; a1=1946e9dbaffj81t8hz5dpp8ev02nisty30ie4rudo50000293795; webId=dc38b0cf2c123a5bbdf2b619475abe68; web_session=030037a0bb88ef7776dcd79af0204a189470f2; gid=yj4KdjfS4qqqyj4KdjfD08F7iiVYy9Yxu2fU3flUYdh8Jd28I3M9v4888JjqWj280j2iyYd4; webBuild=4.62.3; xsecappid=xhs-pc-web; acw_tc=0a0bb13817471005496643594e344269c2251859a1d59682ff1f6ed15910b8; loadts=1747101562272; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=7fa57343-1d8c-48db-9863-0684fcf4b5e0; unread={%22ub%22:%2268045583000000001c0093b7%22%2C%22ue%22:%226800897c000000001201e91d%22%2C%22uc%22:26}',
    }
    source_note_id = link.split("?")[0].replace("https://www.xiaohongshu.com/explore/","")
    xsec_token = link.split("?")[1].split("&")[1].replace("xsec_token=","")
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
    # await gen_headers_sign(headers, "/api/sns/web/v1/feed?" + urlencode(params))
    response = await HttpRequest(url, headers).httpx_post(data=json.dumps(params, separators=(',', ':')))
    print(response.text)

if __name__ == '__main__':
    asyncio.run(
        hongshu_detail(
            "https://www.xiaohongshu.com/explore/68029867000000001200d8c5?note_flow_source=baidu&xsec_token=AB9qOunJ-x94q16s76fcJKKtY36QTc2tBgTdRlovIEwn8=",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            ""
        )
    )