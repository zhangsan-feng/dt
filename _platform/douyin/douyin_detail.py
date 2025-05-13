import asyncio
import httpx
from _platform.douyin.sign import gen_params_sign
from _platform.douyin import douyin_data_handler

async def video_detail(aweme_id, user_agent, cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-_platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'cookie': cookie,
    }

    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'aweme_id': aweme_id,
        'update_version_code': '170400',
        'pc_client_type': '1',
        'pc_libra_divert': 'Windows',
        'support_h265': '1',
        'support_dash': '1',
        'version_code': '190500',
        'version_name': '19.5.0',
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
        'round_trip_time': '50',
    }
    await gen_params_sign(headers, params)
    # print(json.dumps(params, ensure_ascii=False , indent=4))
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.douyin.com/aweme/v1/web/aweme/detail/', params=params, headers=headers)
    # print(response)
    if response:
        json_response = response.json()["aweme_detail"]
        # print(json_response)
        await douyin_data_handler(json_response, headers)


if __name__ == '__main__':
    '''
    live 动态
    0.28 江西的饭怎么能这么辣🥹 # livephoto # 随拍  https://v.douyin.com/pCAV6RWTeQo/ 复制此链接，打开抖音搜索，直接观看视频！ 08/09 iPX:/ F@u.fo
    https://www.douyin.com/note/7486062640565882151
    
    视频
    5.64 05/13 h@o.Dh lpQ:/ 不看牙口挑战3.0 # 永劫无间 # 季莹莹 # cos # 直播录屏分享  https://v.douyin.com/ZKT-e87IvdU/ 复制此链接，打开Dou音搜索，直接观看视频！
    https://www.douyin.com/video/7470885299535629622
    
    图片
    5.17 06/03 A@g.Bt Nws:/ 右滑帮学姐摘眼镜# 永劫无间 # 顾清寒 # 春日序曲 # cos # 壁纸  https://v.douyin.com/cxvBbjQLlxg/ 复制此链接，打开Dou音搜索，直接观看视频！
    https://www.douyin.com/note/7476688986325486887
    
    图片
    1.58 复制打开抖音，看看【絮辰的图文作品】# 动漫少女 # 动漫女头 # 二次元 # 女生头... https://v.douyin.com/945qoAywnMI/ 05/16 o@q.rE aaA:/
    '''
    asyncio.run(
        video_detail(
            "",
            "",
            ""
        )
    )