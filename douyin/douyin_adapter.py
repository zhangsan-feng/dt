import httpx
from douyin.douyin_detail import video_detail
from douyin.douyin_post import douyin_post
from entity.config_enetity import config



async def douyin_adapter(link, user_agent):

    if "v.douyin.com" in link:
        async with httpx.AsyncClient() as client:
            response = await client.get(link, headers={"User-Agent": user_agent})
            print(response.headers.get("location"))
            link = response.headers.get("location")

    if "douyin.com/video/" in link:
        aweme_id = link.replace("https://www.douyin.com/video/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, config.douyin_cookie)

    if "douyin.com/note/" in link:
        aweme_id = link.replace("https://www.douyin.com/note/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, config.douyin_cookie)

    if "iesdouyin.com/share/video/" in link:
        print(config.douyin_cookie)
        aweme_id = link.replace("https://www.iesdouyin.com/share/video/","").split("?")[0].replace("/","")
        return await video_detail(aweme_id, user_agent, config.douyin_cookie)

    if "douyin.com/user" in link:
        sec_user_id = link.replace("https://www.douyin.com/user/","").split("?")[0].replace("/", "")
        return await douyin_post(sec_user_id, user_agent, config.douyin_cookie)

    if "live.douyin.com" in link:
        pass
    if "webcast.amemv.com" in link:
        pass


    if "https://www.douyin.com/user/self?from_tab_name=main&showTab=like" in link:
        pass
    if "https://www.douyin.com/user/self?from_tab_name=main&showTab=favorite_collection" in link:
        pass