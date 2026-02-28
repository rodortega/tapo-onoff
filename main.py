from fastapi import FastAPI
import json
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from tapo import ApiClient

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError("Set USERNAME and PASSWORD in .env")

devices_path = os.path.join(os.path.dirname(__file__), "devices.json")
if not os.path.exists(devices_path):
    raise RuntimeError("devices.json not found")

with open(devices_path, "r") as f:
    try:
        DEVICES = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load devices.json: {e}")

if not isinstance(DEVICES, list):
    raise RuntimeError("devices.json must contain a JSON array of device identifiers")


app = FastAPI(title="tapo-fastapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.tapo_client = ApiClient(USERNAME, PASSWORD)
    try:
        yield
    finally:
        client = getattr(app.state, "tapo_client", None)
        if client:
            close = getattr(client, "close", None)
            if callable(close):
                res = close()
                if hasattr(res, "__await__"):
                    await res


app.router.lifespan_context = lifespan


@app.get("/")
async def root():
    return {"ok": True, "message": "tapo FastAPI service"}


async def switch_devices(action: str):
    client: ApiClient = app.state.tapo_client
    results = []
    for dev in DEVICES:
        try:
            device = await client.p110(dev)
            if action == "on":
                await device.on()
            else:
                await device.off()
            results.append({"device": dev, "status": action, "info": await device.get_device_info_json()})
        except Exception as e:
            results.append({"device": dev, "status": "error", "error": str(e), "traceback": repr(e)})
    return {"action": action, "results": results}


@app.post("/switch/on")
async def switch_on():
    return await switch_devices("on")


@app.post("/switch/off")
async def switch_off():
    return await switch_devices("off")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)