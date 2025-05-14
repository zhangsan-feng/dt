# https://github.com/Cloxl/xhshow
# https://github.com/cv-cat/Spider_XHS
import math
import execjs
from _platform.hongshu.sign.xs_comm import XscEncrypt
from _platform.hongshu.sign.xs import XsEncrypt
from _platform.hongshu.sign.sign_other import MiscEncrypt
from utils import *


current_file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(current_file_path)
# print(project_dir)

async def gen_headers_sign(headers, api, params=""):
    a1 = get_cookie_key(headers["cookie"], "a1")

    try:
        js = execjs.compile(open(project_dir + '/xhs_xs_xsc_56.js', 'r', encoding='utf-8').read())
    except:
        js = execjs.compile(open(project_dir + '_platform/hongshu/sign/xhs_xs_xsc_56.js', 'r', encoding='utf-8').read())

    try:
        xray_js = execjs.compile(open(project_dir + '/xhs_xray.js', 'r', encoding='utf-8').read())
    except:
        xray_js = execjs.compile(open(project_dir + '_platform/hongshu/sign/xhs_xray.js', 'r', encoding='utf-8').read())


    x_b3_traceid = ""
    for t in range(32):
        x_b3_traceid += "abcdef0123456789"[math.floor(16 * random.random())]

    ret = js.call('get_request_headers_params',api, params, a1)
    xs, xt, xs_common = ret['xs'], ret['xt'], ret['xs_common']

    headers["x-s"] = xs
    headers["x-t"] = str(xt)
    headers["x-s-common"]     = xs_common
    headers["x-b3-traceid"]   = x_b3_traceid
    headers["x-xray-traceid"] = xray_js.call('traceId')

