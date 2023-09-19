from fastapi import FastAPI
from db import engine
from sqlmodel import SQLModel
from routers import data


app=FastAPI(title="Products")
app.include_router(data.router)



@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)











