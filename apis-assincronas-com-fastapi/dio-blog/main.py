from fastapi import FastAPI

app = FastAPI()

@app.get('/posts/{framework}')
def read_posts(framework: str):
  return {'posts': [
    { 'title': f'Criando uma aplicação com {framework}' },
    { 'title': f'Arquitetura limpa com {framework}' }
  ]
}