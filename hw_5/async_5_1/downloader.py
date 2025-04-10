import asyncio
import aiohttp
import aiofiles
import sys


async def download_image(session: aiohttp.ClientSession, output_dir: str, semaphore: asyncio.Semaphore, inx: int):
    url = f"https://picsum.photos/id/{inx}/200/300"
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    filename = f"{output_dir}/{inx}.jpg"
                    data = await response.read()
                    async with aiofiles.open(filename, "wb") as file:
                        await file.write(data)
                    print(f"Downloaded: {inx}.jpg")
        except Exception as e:
            print(f"Error downloading image {inx}: {e}")


async def download_images(count: int):
    output_dir = "../artifacts/images_5_1/"
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, output_dir, semaphore, i + 1) for i in range(count)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python downloader.py <number_of_images>")
        sys.exit(1)
    try:
        count = int(sys.argv[1])
        if count <= 0:
            raise ValueError
    except ValueError:
        print("Error: Please provide a positive integer")
        sys.exit(1)

    asyncio.run(download_images(count))
