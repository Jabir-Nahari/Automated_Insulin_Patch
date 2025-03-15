import temperature_sensor_controller
import asyncio
async def main():
    await temperature_sensor_controller.sensing_loop()

if __name__ == "__main__":
    asyncio.run(main())