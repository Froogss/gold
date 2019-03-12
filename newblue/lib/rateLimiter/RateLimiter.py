import asyncio

import aiohttp


class LimitedStructure:
    def __init__(self, max_bucket, period):
        self.period = period
        self.max_bucket = max_bucket
        self.bucket = max_bucket
        self.bucket_refresh_instance = asyncio.create_task(self.bucket_refresh())

    async def bucket_refresh(self):
        while True:
            await asyncio.sleep(self.period)
            self.bucket = self.max_bucket


class Endpoint(LimitedStructure):
    def __init__(self, max_bucket, period):
        self.queue = asyncio.Queue()
        super().__init__(max_bucket, period)

    async def _call(self, future, full_url):
        self.bucket -= 1
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as resp:
                future.set_result(await resp.json())

        # This method should be overwritten to actually call the endpoint

    async def call(self, args):
        # This creates a future comprised of the function to be caed and the arguments to be suppied to said function
        # This future will be pulled from a queue, the function executed and the result of the future set to the result of the function
        queued_future = asyncio.get_event_loop().create_future()
        self.queue.put_nowait((queued_future, self._call(), args))
        return await queued_future


class Service(LimitedStructure):
    def __init__(self, max_bucket, period):
        super().__init__(max_bucket, period)


class Application(LimitedStructure):
    def __init__(self, max_bucket, period):
        super().__init__(max_bucket, period)

    async def check_queued_items(self):
        for service in self.services:
            if service.bucket > 0:
                for endpoint in service.endpoints:
                    if endpoint.queue.qsize > 0 and endpoint.bucket > 0:
                        item = endpoint.queue.get_nowait()
                        await asyncio.create_task(item[1](item[0], item[2]))


class ExampleEndpoint(Endpoint):
    async def _call(self, future, args):
        full_url = args[0]
        await super()._call(future, full_url)
