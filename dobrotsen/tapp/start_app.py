import datetime

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config import path
from dobrotsen.tapp.routers import pages_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=f"{path}/dobrotsen/tapp/static"), name="static")
app.include_router(pages_router, tags=["page"])