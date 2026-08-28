import asyncio
from _platform.douyin.api.douyin_detail_api import video_detail as _video_detail
from _platform.douyin.api.douyin_live_api import douyin_live as _douyin_live
from _platform.douyin.api.douyin_post_api import douyin_post as _douyin_post
from _platform.douyin.browser import handle_detail_with_browser as _handle_detail_with_browser
from _platform.douyin.browser import handle_post_with_browser as _handle_post_with_browser
from config import Configuration
from utils.browser import BrowserObject
from utils.logger import logger as _logger


__all__ = ['douyin_adapter_api', 'douyin_adapter_browser']


_browser = BrowserObject()


async def douyin_adapter_browser(link):
    if "douyin.com/user/" in link or "iesdouyin.com/share/user/" in link:
        return await _handle_post_with_browser(link)

    result = await _browser.browser_request(link)

    if "v.douyin.com" in link:
        response = result.get('response') or {}
        link = response.get('url') or link

    if "douyin.com/video/" in link:
        aweme_id = link.replace("https://www.douyin.com/video/","").split("?")[0].replace("/","")
        return await _handle_detail_with_browser(aweme_id)

    if "douyin.com/note/" in link:
        aweme_id = link.replace("https://www.douyin.com/note/","").split("?")[0].replace("/","")
        return await _handle_detail_with_browser(aweme_id)

    if "iesdouyin.com/share/video/" in link:
        aweme_id = link.replace("https://www.iesdouyin.com/share/video/","").split("?")[0].replace("/","")
        return await _handle_detail_with_browser(aweme_id)

    if "iesdouyin.com/share/note/" in link:
        aweme_id = link.replace("https://www.iesdouyin.com/share/note/","").split("?")[0].replace("/","")
        return await _handle_detail_with_browser(aweme_id)

    if "iesdouyin.com/share/slides/" in link:
        aweme_id = link.replace("https://www.iesdouyin.com/share/slides/","").split("?")[0].replace("/","")
        return await _handle_detail_with_browser(aweme_id)


async def douyin_adapter_api(link):
    result = await _browser.browser_request(link)
    request = result.get('request') or {}
    browser_headers = dict(request.get('headers') or {})

    if "v.douyin.com" in link:
        response = result.get('response') or {}
        link = response.get('url') or link

    cookie = Configuration().douyin_cookie
    browser_headers["cookie"] = cookie

    # if "douyin.com/video/" in link:
    #     aweme_id = link.replace("https://www.douyin.com/video/","").split("?")[0].replace("/","")
    #     return await _video_detail(aweme_id, user_agent, cookie)
    #
    # if "douyin.com/note/" in link:
    #     aweme_id = link.replace("https://www.douyin.com/note/","").split("?")[0].replace("/","")
    #     return await _video_detail(aweme_id, user_agent, cookie)
    #
    # if "iesdouyin.com/share/video/" in link:
    #     aweme_id = link.replace("https://www.iesdouyin.com/share/video/","").split("?")[0].replace("/","")
    #     return await _video_detail(aweme_id, user_agent, cookie)
    #
    # if "iesdouyin.com/share/note/" in link:
    #     aweme_id = link.replace("https://www.iesdouyin.com/share/note/","").split("?")[0].replace("/","")
    #     return await _video_detail(aweme_id, user_agent, cookie)
    #
    # if "iesdouyin.com/share/slides/" in link:
    #     aweme_id = link.replace("https://www.iesdouyin.com/share/slides/","").split("?")[0].replace("/","")
    #     return await _video_detail(aweme_id, user_agent, cookie)
    #
    # if "douyin.com/user" in link:
    #     sec_user_id = link.replace("https://www.douyin.com/user/","").split("?")[0].replace("/", "")
    #     return await _douyin_post(sec_user_id, user_agent, cookie)
    #
    # if "iesdouyin.com/share/user/" in link:
    #     sec_user_id = link.replace("https://www.iesdouyin.com/share/user/","").split("?")[0].replace("/", "")
    #     return await _douyin_post(sec_user_id, user_agent, cookie)
    #
    # if "live.douyin.com" in link or "webcast.amemv.com" in link:
    #     await _douyin_live(link, cookie, user_agent)
    #
    #
    #
    # if "https://www.douyin.com/user/self?from_tab_name=main&showTab=like" in link:
    #     pass
    # if "https://www.douyin.com/user/self?from_tab_name=main&showTab=favorite_collection" in link:
    #     pass

    pass


if __name__ == '__main__':

    # for link in [
    #     "https://v.douyin.com/OCFtqmB1deE/" ,
    #     "https://v.douyin.com/eAFvtkuq8dM/" ,
    #     "https://v.douyin.com/AxBinfaYolc/",
    #     "5.38 复制打开抖音，看看【半分酥.的作品】嘻嘻  https://v.douyin.com/u5FrdENm_r8/ oDu:/ j@C.HI 03/12 :0pm",
    #     "2.33 复制打开抖音，看看【Mr_z的图文作品】# 梅凝 # 凡人修仙传 # 音乐分享 # 自拍  https://v.douyin.com/sCAyVoQTdlQ/ 06/28 :2pm mQX:/ F@h.BG",
    #     "2.35 复制打开抖音，看看【小萱在不在的作品】没有给任何人好脸色的义务  https://v.douyin.com/WCN87R7eXtQ/ :3pm 10/15 i@P.xs fbN:/",
    #     "5.64 复制打开抖音，看看【蕗的作品】以前有个动画片 叫海绵什么来着 # kisskis... https://v.douyin.com/i_Wbwm0SVno/ 06/19 :9pm R@k.Cu reB:/"
    # ]:
    #     asyncio.run(douyin_adapter_browser(link))



    for link in [
        "https://www.douyin.com/user/MS4wLjABAAAAeRcYu7tTuRg1cQrbLYXsD7ogs0AtUSTM__rgb1lk6bk",
        "https://www.douyin.com/user/MS4wLjABAAAA3nZWMFY7d-1ffxBxw_NWXnBJ-gAucmqfuovc7C6AocI",
        "https://www.douyin.com/user/MS4wLjABAAAA3XNy70giFoK4bZR8JKmEZrkyI66yAsQvv1UROAILi24",
        "https://www.douyin.com/user/MS4wLjABAAAAlZuXpbX_sfm-aIqCZnun7hkDAoaL1j1h4yu0tEs-yd8",
        "https://www.douyin.com/user/MS4wLjABAAAAMeTQRwXqRFQPWgwUX72o6fSVq6z5-0gcCpL5T3uKXIE",
        "https://www.douyin.com/user/MS4wLjABAAAAkveHAA4vWmCQRw_-A62QP1Xt7LQbj0yj4hVIgu_r06U",
    ]:
        asyncio.run(douyin_adapter_browser(link))


    pass
