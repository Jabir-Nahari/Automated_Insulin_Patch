# import temperature_sensor_controller as tsc
import pump_controller as pc
import cooler_controller as cc
import asyncio
async def main():
    # temp_controller = tsc.TemperatureSensor(35)
    task1 = asyncio.create_task(pc.run_pump())
    task2 = asyncio.create_task(cc.cooler_loop())
    # task3 = asyncio.create_task(temp_controller.temperature_check())
    # task4 = asyncio.create_task(temp_controller.store_temperature())
    await asyncio.wait([task1, task2],return_when=asyncio.ALL_COMPLETED)

if __name__ == "__main__":
    asyncio.run(main())