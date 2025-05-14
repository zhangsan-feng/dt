import asyncio

from _platform.hongshu.hongshu_detail import hongshu_detail
from _platform.hongshu.hongshu_post import hongshu_post
from config import Config
from utils.http_utls import HttpRequest

async def hongshu_adapter(link, user_agent):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Cookie': 'acw_tc=0ad523af17472027045742387e456d1267870f7fecaa8c83c8dd0aa2553d4c',
    }

    if "xhslink" in link:
        response = await HttpRequest(link, headers).aiohttp_get()
        print(response.url)
        link = str(response.url)

    config = Config()

    if "xiaohongshu.com/explore/" in link:
        await hongshu_detail(link, user_agent, config.hongshu_cookie)

    if "xiaohongshu.com/discovery/item/" in link:
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
    l = "xiaohongshu.com/discovery/item/"
    b = "https://www.xiaohongshu.com/discovery/item/6823e8c9000000002202de61?app_platform=android&ignoreEngage=true&app_version=8.82.0&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBX1U_D0uLpjYGaxnWHhXIhFdJNKJ1K6ijZ39T1tBvzww%3D&author_share=1&xhsshare=CopyLink&shareRedId=ODZERUg9NEA2NzUyOTgwNjY0OTc8Pj8-&apptime=1747202182&share_id=60e983d7021943609798e5733e3c111e&share_channel=copy_link"

    print(l in b)