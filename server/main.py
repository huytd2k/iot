from fastapi import FastAPI
import asyncio
from influxdb import InfluxDBClient

loop = asyncio.get_event_loop()
# client_influx = InfluxDBClient(host="localhost", port=8086)
# client_influx.create_database("data")


class Runner:
    def __init__(self) -> None:
        self.a = 0
        pass

    async def check_api(self):
        while True:
            # Do API check, helps if this is using async methods
            await asyncio.sleep(10)  # 15 minutes (in seconds)
            self.a += 1


runner = Runner()

app = FastAPI()


@app.on_event("startup")
async def start():
    asyncio.create_task(runner.check_api())
    asyncio.run


@app.get("/")
async def root():
    return {"message": f"a = {runner.a}"}
