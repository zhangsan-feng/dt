import asyncio

lock = asyncio.Lock()
M = {}

async def func(uuid):
    for i in range(10):
        print(f"running uuid{uuid} i:{i}")
        await asyncio.sleep(1)


async def create(fn, uuid, link):
    async with lock:
        if uuid in M and M[uuid]["pid"].done():
            return
        pid = asyncio.create_task(fn)
        M[uuid] = {
            "pid": pid,
            "link": link,
            "status":"运行中"
        }


async def query():
    async with lock:
        data = []
        for uuid, ptr in M.items():
            data.append({
                "uuid":uuid,
                "link": ptr["link"],
                "status": "下载完成" if ptr["pid"].done() else "运行中",
            })
        return data


async def kill(uuid):
    async with lock:
        if not M[uuid]["pid"].done():
            M[uuid]["pid"].cancel()
            M[uuid]["status"] = "暂停"


async def kill_all():
    async with lock:
        for uuid, ptr in M.items():
            if not M[uuid]["pid"].done():
                M[uuid]["pid"].cancel()
                M[uuid]["status"] = "暂停"


async def edit(uuid):
    async with lock:
        pass


async def main():
    await create(func(10), 10, "2b")
    await create(func(20), 20, "2b")

    while True:
        print(await query())
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())