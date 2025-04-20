import temperature_sensor_controller as tsc
import asyncio
async def main():
    temp_controller = tsc.temprature_sensor(35)
    task1 = asyncio.create_task(temp_controller.temprature_check())
    task2 = asyncio.create_task(temp_controller.store_temprature())
    await asyncio.wait([task1, task2],timeout=10,return_when=asyncio.ALL_COMPLETED)

if __name__ == "__main__":
    asyncio.run(main())