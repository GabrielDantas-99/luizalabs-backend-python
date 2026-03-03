from contextlib import asynccontextmanager

import sqlalchemy as sa
from fastapi import FastAPI
from controllers import post
import databases

DATABASE_URL = 'sqlite:///./blog.db'

database = databases.Database(DATABASE_URL)
engine = sa.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata = sa.MetaData()
metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
  await database.connect()
  yield
  await database.disconnect()
  

app = FastAPI()
app.include_router(post.router)