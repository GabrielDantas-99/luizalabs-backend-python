from contextlib import asynccontextmanager

import sqlalchemy as sa
from fastapi import FastAPI
from src.database import database
from src.controllers import post


@asynccontextmanager
async def lifespan(app: FastAPI):
  await database.connect()
  yield
  await database.disconnect()
  

app = FastAPI()
app.include_router(post.router)