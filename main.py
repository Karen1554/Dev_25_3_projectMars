from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles

import bucket
import appoinment
import pet
import estudiantes
import user
import vet
from db import create_tables, init_db
##from pet import APIRouter

##Clever
from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield



app = FastAPI(lifespan=lifespan, title="Pet API")

app.mount("/static", StaticFiles(directory="bucket"), name="static")
app.include_router(pet.router, tags=["pet"], prefix="/pets")
app.include_router(user.router, tags=["user"], prefix="/users")
app.include_router(vet.router, tags=["vet"], prefix="/vets")
app.include_router(appoinment.router, tags=["appointment"], prefix="/appointments")
#app.include_router(estudiantes.router, tags=["estudiantes"], prefix="/estudiantes" )

@app.post("/bucket")
async def save_bucket (file: UploadFile = File(...)):
    result = await bucket.upload_file(file)
    return result


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

