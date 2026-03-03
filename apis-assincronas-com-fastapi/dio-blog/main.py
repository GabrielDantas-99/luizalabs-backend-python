from datetime import UTC, datetime

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

fake_db = [
    { 'title': 'Criando uma aplicação com FastAPI', 'published': True },
    { 'title': 'Arquitetura limpa com FastAPI', 'published': False },
    { 'title': 'Criando uma aplicação com Spring Boot', 'published': True },
    { 'title': 'Arquitetura limpa com Spring Boot', 'published': True },
]

class Post(BaseModel):
  title: str
  date: datetime = datetime.now(UTC)
  published: bool = False
  
@app.post('/posts/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
  fake_db.append(post.model_dump())
  return post

@app.get('/posts/')
def read_posts(published: bool, limit: int, skip: int = 0):
  return [
    post for post in fake_db[skip : skip + limit] 
    if post['published'] is published
  ]

@app.get('/posts/{framework}')
def read_framework_posts(framework: str):
  return {'posts': [
    { 'title': f'Criando uma aplicação com {framework}' },
    { 'title': f'Arquitetura limpa com {framework}' }
  ]
}