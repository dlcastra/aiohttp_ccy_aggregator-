import asyncio
import json
import time

from app.utils import rate_analysis


async def main():
    with open("stress_test_data.json", "r") as file:
    # with open("test_data.json", "r") as file:
        rates = json.load(file)

    start_time = time.perf_counter()
    result = await rate_analysis(rates)
    end_time = time.perf_counter()

    print(result)
    print(f"Run time: {end_time - start_time:.4f} sec")


asyncio.run(main())
