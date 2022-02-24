from email.mime import base
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from influxdb_client import InfluxDBClient
from pydantic import BaseModel


app = FastAPI()
db = []


app.mount("/static", StaticFiles(directory="statics"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/devices/{did}", response_class=HTMLResponse)
async def device_page(request: Request, did: str):
    return templates.TemplateResponse("item.html", {"request": request, "did": did})

@app.get("/addPatient", response_class=HTMLResponse)
async def device_page(request: Request):
    return templates.TemplateResponse("add_patient.html", {"request": request})


@app.get("/api/heartbeat/device/{did}")
async def get_heartbeat(did: str):
    dbclient = InfluxDBClient(
        "http://localhost:8086",
        token="BCzq6pkHR96UjaMbqys78hsHG8IaaJ6Ij9TjiJd_u-I7Bt3-tTPx68tvpbyve-unCEEGrjqDtGLi_SxaFAlRTw==",
    )
    query = dbclient.query_api()
    tables = query.query(f"""
            from(bucket: "iot")
            |> range(start: -3m)
            |> filter(fn: (r) => r["_measurement"] == "heartbeat")
            |> filter(fn: (r) => r["_field"] == "heartbeat")
            |> filter(fn: (r) => r["device"] == "{did}")
            |> yield(name: "mean") 
    """, org="iot")
    return tables[0]


class Patient(BaseModel):
    device_id: str
    doctor_email: str
    heartrate_threshhold: int
    

@app.post("/api/patient")
async def create_patient(patient: Patient):
    db.append(patient.dict())
    return patient.dict()


@app.get("/api/patient/{device_id}")
async def get_patient(device_id: str):
    p = [a for a in db if a['device_id'] == device_id]
    return p[0] if p else None