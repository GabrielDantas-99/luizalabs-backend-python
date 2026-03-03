from fastapi import FastAPI

app = FastAPI()

fake_db = [
    { 'title': 'Criando uma aplicação com FastAPI', 'published': True },
    { 'title': 'Arquitetura limpa com FastAPI', 'published': False },
    { 'title': 'Criando uma aplicação com Spring Boot', 'published': True },
    { 'title': 'Arquitetura limpa com Spring Boot', 'published': True },
  ]

@app.get('/posts')
def read_posts(published: bool, skip: int = 0, limit: int = len(fake_db)):
  return [post for post in fake_db[skip: skip + limit] if post['published'] is published]

@app.get('/posts/{framework}')
def read_framework_posts(framework: str):
  return {'posts': [
    { 'title': f'Criando uma aplicação com {framework}' },
    { 'title': f'Arquitetura limpa com {framework}' }
  ]
}