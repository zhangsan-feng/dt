# https://github.com/Cloxl/xhshow

from _platform.hongshu.sign.xs_comm import XscEncrypt
from _platform.hongshu.sign.xs import XsEncrypt
from _platform.hongshu.sign.sign_other import MiscEncrypt
from utils import *
import time





async def gen_headers_sign(headers, params):
    a1 = get_cookie_key(headers["cookie"], "a1")

    b1 = ""
    ts = str(int(time.time() * 1000))
    xs = await XsEncrypt.encrypt_xs(params, a1, ts)

    print(xs)

    headers["x-s"] = xs
    # headers["x-t"] = ""
    # headers["x-s-common"]     = XscEncrypt.encrypt_xsc()
    # headers["x-b3-traceid"]   = MiscEncrypt.x_b3_traceid()
    # headers["x-xray-traceid"] = MiscEncrypt.x_xray_traceid()

