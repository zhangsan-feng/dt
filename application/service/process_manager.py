import asyncio

lock = asyncio.Lock()
M = {}

MAX_CONCURRENT_TASKS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

async def create(fn, uuid, link):
    async with lock:

        if uuid in M:
            old_task = M[uuid]["pid"]
            old_task.cancel()
            try:
                await old_task
            except asyncio.CancelledError:
                pass

        await semaphore.acquire()

        async def wrapped_task():
            try:
                await fn
            finally:
                semaphore.release()
                async with lock:
                    if uuid in M:
                        M[uuid]["status"] = "已完成"

        pid = asyncio.create_task(wrapped_task())
        M[uuid] = {
            "pid": pid,
            "link": link,
            "status": "运行中"
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


async def func(uuid):
    for i in range(10):
        print(f"running uuid{uuid} i:{i}")
        await asyncio.sleep(1)


async def main():
    for i in range(20):
        await create(func(i), i, "2b")

    while True:
        print(await query())
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())