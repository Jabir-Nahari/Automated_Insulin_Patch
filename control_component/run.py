import temperature_sensor_controller as tsc
import asyncio
async def main():
    task1 = asyncio.create_task(tsc.temprature_check)
    task2 = asyncio.create_task(tsc.store_temprature)
    asyncio.wait([task1, task2],return_when=asyncio.ALL_COMPLETED)

if __name__ == "__main__":
    asyncio.run(main())