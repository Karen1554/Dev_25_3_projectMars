from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
import appoinment
import pet
import estudiantes
import user
import vet
import images
from db import create_tables


##from pet import APIRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(app)
    yield


app = FastAPI(lifespan=lifespan, title="Pet API")

app.mount("/img", StaticFiles(directory="upload"), name="img")
app.include_router(pet.router, tags=["pet"], prefix="/pets")
app.include_router(user.router, tags=["user"], prefix="/users")
app.include_router(vet.router, tags=["vet"], prefix="/vets")
app.include_router(appoinment.router, tags=["appointment"], prefix="/appointments")


# app.include_router(estudiantes.router, tags=["estudiantes"], prefix="/estudiantes" )


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await images.upload_file(file)
    return result


@app.get("/", response_class=HTMLResponse, status_code=200)
async def root():
    return """
    <html>
    <head>
    </head>
    <body>
    <h1>Pet API</h1>
    </body>
    </html>
    
    """


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
