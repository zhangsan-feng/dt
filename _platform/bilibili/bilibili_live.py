import asyncio


async def bilibili_live(link, user_agent):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://live.bilibili.com/',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://live.bilibili.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent':user_agent,
    }


    # room_id =  url.split("?")[0].replace("https://live.bilibili.com/","")

    # params = {
    #     "room_id":room_id,
    #     "mask":"1",
    #     "qn":"0",
    #     "platform":"web",
    #     "protocol":"0,1",
    #     "format":"0,1,2",
    #     "codec":"0,1,2",
    #     "dolby":"5",
    #     "panorama":"1",
    # }

    url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo"

    # console.log(response_body)
    # const info = response_body['data']["playurl_info"]["playurl"]["stream"][0]["format"][0]["codec"][0]
    # const uids = response_body['data']["uid"].toString()
    # const flv_stream_url = info["url_info"][0]["host"] + info["base_url"] + info["url_info"][0]["extra"]


    # params = {
    #     "uids":uids,
    #     "req_biz":"video"
    # }
    # url = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"


    # author = word_analysis(response_body['data']["by_uids"][uids]["uname"])
    # title = word_analysis(response_body['data']["by_uids"][uids]["title"])
    # flv_file_name = nickname + '_' + GetTime()+ ".flv"









if __name__ == '__main__':
    asyncio.run(
        bilibili_live(

        )
    )