import asyncio
import json
import httpx


async def gen_tt_wid():
    request_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-_platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    }

    request_url = "https://ttwid.bytedance.com/ttwid/union/register/"
    request_params = {
        "region":"cn",
        "aid":1768,
        "needFid":False,
        "service":"www.ixigua.com",
        "migrate_info":{"ticket":"","source":"node"},
        "cbUrlProtocol":"https",
        "union":True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=request_url,data=json.dumps(request_params), headers=request_headers)
        print(response.headers)
        print(response.headers.get("set-cookie"))


if __name__ == '__main__':
    asyncio.run(gen_tt_wid())