import asyncio
import json
import httpx

async def gen_web_id():
    request_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    }

    request_url = "https://mcs.zijieapi.com/webid"
    request_params = {
        "app_id": 6383,
        "referer": "https://www.douyin.com/",
        "url": "https://www.douyin.com/",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "user_unique_id": "",
    }
    data = {
        "app_id": 6383, "url": "https://www.douyin.com/",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "referer": "https://www.douyin.com/", "user_unique_id": ""}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=request_url, data=json.dumps(data), params=request_params,
                                     headers=request_headers)
        # print(response.json()['web_id'])
    return response.json()['web_id']


if __name__ == '__main__':
    asyncio.run(gen_web_id())
