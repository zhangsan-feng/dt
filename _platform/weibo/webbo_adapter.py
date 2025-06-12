from _platform.weibo.weibo_detail import weibo_detail
from _platform.weibo.weibo_feed import weibo_user_feed
from _platform.weibo.weibo_home import weibo_user_home
from _platform.weibo.weibo_image import weibo_user_image
from _platform.weibo.weibo_video import weibo_user_video
from application.entity.config_entity import ConfigEntityObject

async def weibo_adapter(link, user_agent):
    c = ConfigEntityObject()

    if link in "https://weibo.com/tv/show/":
        pass
    if link in "tabtype=home":
        await weibo_user_home(link, user_agent, c.weibo_cookie)
    if link in "tabtype=feed":
        await weibo_user_feed(link, user_agent, c.weibo_cookie)
    if link in "tabtype=newVideo":
        await weibo_user_video(link, user_agent, c.weibo_cookie)
    if link in "tabtype=album":
        await weibo_user_image(link, user_agent, c.weibo_cookie)
    if link in "weibo.com/u/":
        await weibo_user_feed(link, user_agent, c.weibo_cookie)
    if link in "weibo.com":
        await weibo_detail(link, user_agent, c.weibo_cookie)

