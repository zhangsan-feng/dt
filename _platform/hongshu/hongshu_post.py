import asyncio
from utils import random_sleep
from _platform.hongshu.sign import gen_headers_sign
from utils.http_utls import HttpRequest
from urllib.parse import parse_qs, urlencode
from _platform.hongshu.hongshu_detail import hongshu_detail


async def hongshu_post(link, user_agent, cookie):
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/user_posted"
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

    user_id = link.split("?")[0].replace("https://www.xiaohongshu.com/user/profile/", "")
    xsec_token = parse_qs(link.split("?")[1])["xsec_token"][0]
    xsec_source = parse_qs(link.split("?")[1])["xsec_source"][0]
    params = {
        "num":30,
        "cursor":"",
        "user_id":user_id,
        "image_formats":"jpg,webp,avif",
        "xsec_token":xsec_token,
        "xsec_source":xsec_source
    }
    while True:
        await gen_headers_sign(headers, "/api/sns/web/v1/user_posted?" + urlencode(params))
        response = await HttpRequest(url + "?" + urlencode(params) , headers).httpx_get()
        # print(response.text)
        response_body = response.json()["data"]
        params["cursor"] = response_body["cursor"]

        for data in response_body["notes"]:
            tmp_link = f"https://www.xiaohongshu.com/explore/{data["note_id"]}?xsec_token={data["xsec_token"]}&xsec_source=pc_feed"
            await hongshu_detail(tmp_link, user_agent, cookie)
            random_sleep()

        if response_body["has_more"] == True:
            break


if __name__ == '__main__':
    asyncio.run(
        hongshu_post(
            "https://www.xiaohongshu.com/user/profile/61f6ac5f000000001000f2a7?xsec_token=AB539uiMTwVgrjUR59NtO7MIIB9YqvMTwYdnPabqDaFek=&xsec_source=pc_note",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            ""
        )
    )
