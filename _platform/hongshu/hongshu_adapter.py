import asyncio

from _platform.hongshu.hongshu_detail import hongshu_detail
from _platform.hongshu.hongshu_post import hongshu_post
from config import Config

async def hongshu_adapter(link, user_agent):
    config = Config()
    if "xiaohongshu.com/explore/" in link:

        await hongshu_detail(link, user_agent, config.hongshu_cookie)

    if "xiaohongshu.com/user/profile/" in link:

        await hongshu_post(link, user_agent, config.hongshu_cookie)



if __name__ == '__main__':
    asyncio.run(
        hongshu_adapter(
            "",
           ""
        )
    )