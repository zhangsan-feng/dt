# https://github.com/Johnserf-Seed/f2/blob/main/f2/utils/abogus.py
# https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/main/crawlers/douyin/web/abogus.py
# https://github.com/JoeanAmier/TikTokDownloader/blob/master/src/encrypt/aBogus.py


import asyncio
from http.cookies import SimpleCookie

from _platform.douyin.api.sign import ms_token, verify_fp
from _platform.douyin.api.sign import a_bogus_tk, web_id
from _platform.douyin.api.sign.a_bogus import generate_a_bogus
from utils import get_cookie_key
from utils.logger import logger


def _cookie_value(cookie_header, *names):
    cookie = SimpleCookie()
    try:
        cookie.load(cookie_header or "")
    except (TypeError, ValueError):
        cookie = SimpleCookie()
    for name in names:
        if name in cookie and cookie[name].value:
            return cookie[name].value
    for name in names:
        value = get_cookie_key(cookie_header or "", name)
        if value:
            return value
    return ""


async def _best_effort_web_id(headers):
    try:
        return await web_id.gen_web_id()
    except Exception as exc:
        logger.warning("Douyin web_id generation failed error=%s", type(exc).__name__)
        return ""


async def _best_effort_verify_fp():
    try:
        return await verify_fp.gen_verify_fp()
    except Exception as exc:
        logger.warning("Douyin verifyFp generation failed error=%s", type(exc).__name__)
        return ""

async def gen_params_sign(headers, params):

    params['webid']     = await web_id.gen_web_id()
    params['uifid']     = get_cookie_key(headers["cookie"], "UIFID")
    params['verifyFp']  = get_cookie_key(headers["cookie"], "s_v_web_id")
    params['fp']        = get_cookie_key(headers["cookie"], "s_v_web_id")
    params['msToken']   = await ms_token.gen_ms_token()

    # chrome_fp = a_bogus_f2.BrowserFingerprintGenerator.generate_fingerprint("Chrome")
    # a_bogus = a_bogus_f2.ABogus(headers["user-agent"], chrome_fp).generate_abogus(urlencode(params))[1]
    a_bogus = a_bogus_tk.ABogus(headers['user-agent']).get_value(params)
    params['a_bogus']   = a_bogus

    # headers['uifid']     = cookie.get("UIFID").value



async def gen_detail_params_sign(headers, params, endpoint, screen=None):
    """Build detail-page parameters and sign them with the current pure signer."""

    cookie = headers.get("cookie", "")
    webid = _cookie_value(cookie, "webid", "web_id") or await _best_effort_web_id(headers)
    if webid:
        params['webid'] = webid
    else:
        params.pop('webid', None)

    params['uifid'] = _cookie_value(cookie, "UIFID", "UIFID_TEMP") or ""
    params['verifyFp'] = _cookie_value(cookie, "s_v_web_id", "verifyFp", "verify_fp")
    if not params['verifyFp']:
        params['verifyFp'] = await _best_effort_verify_fp()
    params['fp'] = params['verifyFp']
    token = _cookie_value(cookie, "msToken", "ms_token")
    if not token:
        token = await ms_token.gen_ms_token(headers.get("user-agent"))
    if token:
        params['msToken'] = token
    else:
        params.pop('msToken', None)

    signed_url, a_bogus = await asyncio.to_thread(
        generate_a_bogus,
        endpoint,
        params,
        headers.get("user-agent", ""),
        screen,
    )
    params['a_bogus'] = a_bogus
    return signed_url


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




if __name__ == '__main__':

    asyncio.run(gen_params_sign({}, {}))
