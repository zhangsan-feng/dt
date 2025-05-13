import asyncio
import httpx
from _platform.douyin.sign import gen_params_sign


async def douyin_collect(cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.douyin.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/user/self?from_tab_name=main&showTab=favorite_collection',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-_platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-secsdk-csrf-token': 'DOWNGRADE',
        'cookie': cookie,
    }
    cursor = 0
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'publish_video_strategy_type': '2',
        'pc_client_type': '1',
        'pc_libra_divert': 'Windows',
        'update_version_code': '170400',
        'support_h265': '1',
        'support_dash': '1',
        'version_code': '170400',
        'version_name': '17.4.0',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '135.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '135.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '16',
        'device_memory': '8',
        '_platform': 'PC',
        'downlink': '10',
        'effective_type': '4g',
        'round_trip_time': '100',
    }

    data = {
        'count': '10',
        'cursor': cursor,
    }
    url = 'https://www.douyin.com/aweme/v1/web/aweme/listcollection/'

    await gen_params_sign(headers, params)
    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, params=params, headers=headers, data=data)
    if response:
        print(response.text)

if __name__ == '__main__':
    asyncio.run(
        douyin_collect(
            ""
        )
    )