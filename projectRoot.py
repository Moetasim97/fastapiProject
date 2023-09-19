from fastapi import FastAPI
from db import engine
from sqlmodel import SQLModel
from routers import data
from fastapi.middleware.cors import CORSMiddleware



origins=["http://127.0.0.1:8000"]
app=FastAPI(title="Products")
app.include_router(data.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)


@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)











