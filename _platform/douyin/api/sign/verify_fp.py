import asyncio
import random
import time

async def gen_verify_fp():
    base_str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    t = len(base_str)
    milliseconds = int(round(time.time() * 1000))
    base36 = ""
    while milliseconds > 0:
        remainder = milliseconds % 36
        if remainder < 10:
            base36 = str(remainder) + base36
        else:
            base36 = chr(ord("a") + remainder - 10) + base36
        milliseconds = int(milliseconds / 36)
    r = base36
    o = [""] * 36
    o[8] = o[13] = o[18] = o[23] = "_"
    o[14] = "4"

    for i in range(36):
        if not o[i]:
            n = 0 or int(random.random() * t)
            if i == 19:
                n = 3 & n | 8
            o[i] = base_str[n]
    fp = "verify_" + r + "_" + "".join(o)
    # print(fp)
    return fp

if __name__ == '__main__':
    asyncio.run(gen_verify_fp())