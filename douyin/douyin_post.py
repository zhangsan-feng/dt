import asyncio

import httpx

from douyin import douyin_data_handler
from douyin.sign import gen_params_sign


async def douyin_post(sec_user_id, user_agent, cookie):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/user/' + str(sec_user_id),
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'cookie': cookie,
    }
    max_cursor = 0
    while True:
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'channel': 'channel_pc_web',
            'sec_user_id': sec_user_id,
            'max_cursor': max_cursor,
            'locate_item_id': '7489891376180628790',
            'locate_query': 'false',
            'show_live_replay_strategy': '1',
            'need_time_list': '1',
            'time_list_query': '0',
            'whale_cut_token': '',
            'cut_version': '1',
            'count': '18',
            'publish_video_strategy_type': '2',
            'from_user_page': '1',
            'update_version_code': '170400',
            'pc_client_type': '1',
            'pc_libra_divert': 'Windows',
            'support_h265': '1',
            'support_dash': '1',
            'version_code': '290100',
            'version_name': '29.1.0',
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
            'platform': 'PC',
            'downlink': '10',
            'effective_type': '4g',
            'round_trip_time': '100',
        }

        headers, params = await gen_params_sign(headers, params)
        async with httpx.AsyncClient() as client:
            response = await client.get('https://www.douyin.com/aweme/v1/web/aweme/post/', params=params, headers=headers)
        # print(response.text)

        if response:
            json_response = response.json()["aweme_list"]
            # print(json_response)
            for data in json_response:
                await douyin_data_handler(data, headers)
            if response.json()["has_more"] == 0:
                break
            max_cursor = response.json()["max_cursor"]

if __name__ == '__main__':
    asyncio.run(
        douyin_post(
            "",
            "",
            ""
        )
    )