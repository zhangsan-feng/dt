import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
import aiohttp


class HttpRequest:
    def __init__(self, url, headers, proxy=None):
        self.url = url
        self.proxy = proxy
        self.headers = headers
        self.max_retries = 3
        self.fail_num = 3
        self.timeout = 3

    async def httpx_get(self, params):
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
        async def __get():
            try:
                async with httpx.AsyncClient() as client:
                    return await client.get(self.url, params=params, headers=self.headers)
            except Exception as e:
                print(f"request error: {e}")
                raise
        return await __get()

    async def httpx_post(self, data=None, json=None):
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
        async def __post():
            try:
                async with httpx.AsyncClient() as client:
                    return await client.post(self.url, data=data, json=json, headers=self.headers)
            except Exception as e:
                print(f"request error: {e}")
                raise
        return await __post()


    async def aiohttp_get(self, params):
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
        async def __get():
            try:
                async with aiohttp.ClientSession() as session:
                    return await session.get(self.url, params=params, headers=self.headers)
            except Exception as e:
                print(f"request error: {e}")
                raise
        return await __get()

    async def aiohttp_post(self, data=None, json=None):
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
        async def __post():
            try:
                async with aiohttp.ClientSession() as session:
                    return await session.post(self.url, data=data, json=json, headers=self.headers)
            except Exception as e:
                print(f"request error: {e}")
                raise

        return await __post()

