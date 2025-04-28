import asyncio

import httpx
from _platform.douyin.douyin_detail import video_detail
from _platform.douyin.douyin_live import douyin_live
from _platform.douyin.douyin_post import douyin_post
from config import Config




async def douyin_adapter(link, user_agent):
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
    }
    if "v.douyin.com" in link:
        async with httpx.AsyncClient() as client:
            response = await client.get(link, headers=headers)
            print(response.headers.get("location"))
            link = response.headers.get("location")

    cookie = Config().douyin_cookie
    if "douyin.com/video/" in link:
        aweme_id = link.replace("https://www.douyin.com/video/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, cookie)

    if "douyin.com/note/" in link:
        aweme_id = link.replace("https://www.douyin.com/note/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, cookie)

    if "iesdouyin.com/share/video/" in link:
        aweme_id = link.replace("https://www.iesdouyin.com/share/video/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, cookie)

    if "iesdouyin.com/share/note/" in link:
        aweme_id = link.replace("https://www.iesdouyin.com/share/note/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, cookie)

    if "iesdouyin.com/share/slides/" in link:
        aweme_id = link.replace("https://www.iesdouyin.com/share/slides/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, cookie)

    if "douyin.com/user" in link:
        sec_user_id = link.replace("https://www.douyin.com/user/","").split("?")[0].replace("/", "")
        return await douyin_post(sec_user_id, user_agent, cookie)

    if "live.douyin.com" in link or "webcast.amemv.com" in link:
        await douyin_live(link, cookie, user_agent)



    if "https://www.douyin.com/user/self?from_tab_name=main&showTab=like" in link:
        pass
    if "https://www.douyin.com/user/self?from_tab_name=main&showTab=favorite_collection" in link:
        pass

if __name__ == '__main__':
    asyncio.run(
        douyin_adapter(
            "",
            ""
        )
    )