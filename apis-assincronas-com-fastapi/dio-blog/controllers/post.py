from datetime import UTC, datetime
from typing import Annotated

from fastapi import Header, Response, status, Cookie, APIRouter

from schemas.post import PostIn
from views.post import PostOut

router = APIRouter(prefix="/posts")
  
fake_db = [
    { 'title': 'Criando uma aplicação com FastAPI', 'date': datetime.now(UTC), 'published': True },
    { 'title': 'Arquitetura limpa com FastAPI', 'date': datetime.now(UTC), 'published': False },
    { 'title': 'Criando uma aplicação com Spring Boot', 'date': datetime.now(UTC), 'published': True },
    { 'title': 'Arquitetura limpa com Spring Boot', 'date': datetime.now(UTC), 'published': True },
]
  
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostIn)
def create_post(post: PostIn):
  fake_db.append(post.model_dump())
  return post

@router.get('/', response_model=list[PostOut])
def read_posts(
  response: Response, 
  published: bool, 
  limit: int, 
  skip: int = 0, 
  ads_id: Annotated[str | None, Cookie()] = None,
  user_agent: Annotated[str | None, Header()] = None
):
  response.set_cookie(key="user", value="gabriel@mail.com")
  print(f"Cookie: {ads_id}")
  print(f"User-agent: {user_agent}")
  return [
    post for post in fake_db[skip : skip + limit] 
    if post['published'] is published
  ]

@router.get('/{framework}')
def read_framework_posts(framework: str):
  return {'posts': [
    { 'title': f'Criando uma aplicação com {framework}' },
    { 'title': f'Arquitetura limpa com {framework}' }
  ]
}