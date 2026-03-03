from fastapi import APIRouter, status

from schemas.post import PostIn, PostUpdateIn
from views.post import PostOut
from models.post import posts
from database import database

router = APIRouter(prefix="/posts")

@router.get("/", response_model=list[PostOut])
async def read_posts(published: bool, limit: int, skip: int = 0):
    query = posts.select()
    return await database.fetch_all(query)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    query = posts.insert().values(
        title=post.title, 
        content=post.content, 
        published_at=post.published_at, 
        published=post.published
    )
    last_id = await database.execute(query)
    return {**post.model_dump(), "id": last_id}

