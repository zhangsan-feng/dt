import asyncio
from http.cookies import SimpleCookie
from _platform.douyin.sign import ms_token
from _platform.douyin.sign.a_bogus_tk import ABogus
from utils import get_cookie_key
from utils.http_utls import HttpRequest
from _platform.douyin import douyin_live_handler


async def web(headers, room_id):

    url = "https://live.douyin.com/webcast/room/web/enter/"
    params = {
        'aid': '6383',
        'app_name': 'douyin_web',
        'live_id': '1',
        'device_platform': 'web',
        'language': 'zh-CN',
        'enter_from': 'web_share_link',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '135.0.0.0',
        'web_rid': room_id,
        'room_id_str': room_id,
        'enter_source': '',
        'is_need_double_stream': 'false',
        'insert_task_id': '',
        'live_reason': '',
        'msToken': await ms_token.gen_ms_token(),
    }
    params["a_bogus"] = ABogus(headers["user-agent"]).get_value(params)
    response = await HttpRequest(url, headers).httpx_get(params)
    # print(response.text)

    response_body = response.json()
    # print(response_body)

    author = response_body['data']['user']['nickname']
    title = response_body['data']['data'][0]['title']
    flv_stream_url = response_body['data']["similar_rooms"][0]["room"]["stream_url"]["flv_pull_url"]["FULL_HD1"]

    await douyin_live_handler(author, title, flv_stream_url, headers)

async def app(headers, room_id):
    url = "https://webcast.amemv.com/webcast/room/reflow/info/"
    params = {
            "verifyFp":get_cookie_key(headers["cookie"], "s_v_web_id"),
            "type_id":"0","live_id":"1",
            "room_id":room_id,
            "sec_user_id":room_id,
            "version_code":"99.99.99",
            "app_id":"1128",
        }
    headers["cookie"] = ""
    response = await HttpRequest(url, headers).httpx_get(params)
    # print(response.text)

    response_body = response.json()
    author = response_body['data']["room"]["owner"]["nickname"]
    title = response_body["data"]["room"]["title"]
    stream_url = response_body['data']["room"]["stream_url"]
    flv_stream_url = stream_url["flv_pull_url"]["FULL_HD1"]

    await douyin_live_handler(author, title, flv_stream_url, headers)

async def douyin_live(link, cookie, user_agent):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': link,
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
        'cookie': cookie,
    }

    if "live.douyin.com" in link:
        room_id = link.split("?")[0].replace("https://live.douyin.com/", "")
        await web(headers, room_id)

    if "webcast.amemv.com" in link:
        room_id = link.split("?")[0].replace("https://webcast.amemv.com/douyin/webcast/reflow/", "")
        await app(headers, room_id)




if __name__ == '__main__':

    """
    9- #在抖音，记录美好生活#【带土土（国服艾琳）】正在直播，来和我一起支持Ta吧。复制下方链接，打开【抖音】，直接观看直播！ https://v.douyin.com/H3wlZA9Dyyg/ 3@5.com :2pm
    https://live.douyin.com/82036225582?room_id=7497878603699571467&enter_from_merge=web_share_link&enter_method=web_share_link&previous_page=app_code_link&camera_id=0
    """


    asyncio.run(
        douyin_live(
            "",
            "",
            ""
        )
    )