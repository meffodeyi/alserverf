from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Текущее состояние
device_state = {
    "trigger": False,
    "color": "magenta"
}


# Разрешённые цвета
ALLOWED_COLORS = {
    "magenta",
    "sky_blue",
    "red",
    "blue",
    "purple"
}


class TriggerRequest(BaseModel):
    color: str


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


# ESP32 обращается сюда каждые 5 секунд
@app.get("/api/status")
async def get_status():
    return device_state


# Веб-страница вызывает этот endpoint
@app.post("/api/trigger")
async def trigger(request: TriggerRequest):

    if request.color not in ALLOWED_COLORS:
        return {
            "success": False,
            "error": "Unknown color"
        }

    device_state["trigger"] = True
    device_state["color"] = request.color

    return {
        "success": True,
        "color": request.color
    }


# ESP32 вызывает после получения сигнала
@app.post("/api/ack")
async def acknowledge():

    device_state["trigger"] = False

    return {
        "success": True
    }