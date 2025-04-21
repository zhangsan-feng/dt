# https://github.com/Johnserf-Seed/f2/blob/main/f2/utils/abogus.py
# https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/main/crawlers/douyin/web/abogus.py
# https://github.com/JoeanAmier/TikTokDownloader/blob/master/src/encrypt/aBogus.py


import asyncio
from _platform.douyin.sign import a_bogus_tk, ms_token, web_id
from http.cookies import SimpleCookie


async def gen_params_sign(headers, params):
    cookie = SimpleCookie()
    cookie.load(headers['cookie'])

    params['webid']     = await web_id.gen_web_id()
    params['uifid']     = cookie.get("UIFID").value
    params['verifyFp']  = cookie.get("s_v_web_id").value
    params['fp']        = cookie.get("s_v_web_id").value
    params['msToken']   = await ms_token.gen_ms_token()

    # chrome_fp = a_bogus_f2.BrowserFingerprintGenerator.generate_fingerprint("Chrome")
    # a_bogus = a_bogus_f2.ABogus(headers["user-agent"], chrome_fp).generate_abogus(urlencode(params))[1]
    a_bogus = a_bogus_tk.ABogus(headers['user-agent']).get_value(params)
    params['a_bogus']   = a_bogus

    headers['uifid']     = cookie.get("UIFID").value

    return headers, params

async def gen_like_params_sign(headers, params):
    cookie = SimpleCookie()
    cookie.load(headers['cookie'])

    # params['webid']     = await web_id.gen_web_id()
    # params['uifid']     = cookie.get("UIFID").value
    params['verifyFp']  = cookie.get("s_v_web_id").value
    params['fp']        = cookie.get("s_v_web_id").value
    params['msToken']   = await ms_token.gen_ms_token()

    # chrome_fp = a_bogus_f2.BrowserFingerprintGenerator.generate_fingerprint("Chrome")
    # a_bogus = a_bogus_f2.ABogus(headers["user-agent"], chrome_fp).generate_abogus(urlencode(params))[1]
    a_bogus = a_bogus_tk.ABogus(headers['user-agent']).get_value(params)
    params['a_bogus']   = a_bogus

    headers['uifid']     = cookie.get("UIFID").value

    return headers, params



if __name__ == '__main__':

    asyncio.run(gen_params_sign({}, {}))