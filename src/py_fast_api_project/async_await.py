
import time
import httpx
import asyncio


# Sync
def get_products_sync(TEST_URL):
    start = time.perf_counter()
    products = []

    with httpx.Client(timeout=30.0) as client:
        for i in range(1, 11):
            response = client.get(f"{TEST_URL}{i}")
            response.raise_for_status()

            data = response.json()

            products.append(data["title"])

    elapsed = time.perf_counter() - start

    return {
        "mode": "sync",
        "elapsed_time_sec": round(elapsed, 3),
        "products": products
    }


# Async
async def get_products_async(TEST_URL):
    start = time.perf_counter()
    products = []

    async with httpx.AsyncClient(timeout=30.0) as client:

        responses = await asyncio.gather(
            *(
                client.get(f"{TEST_URL}{i}")
                for i in range(1, 11)
            )
        )

        for response in responses:
            response.raise_for_status()

            data = response.json()

            products.append(data["title"])

    elapsed = time.perf_counter() - start

    return {
        "mode": "async-concurrent",
        "elapsed_time_sec": round(elapsed, 3),
        "products": products
    }
