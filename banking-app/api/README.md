# 🏦 API Bancária

API bancária RESTful assíncrona construída com **FastAPI**, com autenticação JWT, transações de depósito/saque e consulta de extrato de conta.

## Funcionalidades

- ✅ Gerenciamento de contas (criar, listar)
- ✅ Transações: depósitos e saques com validação de saldo
- ✅ Extrato da conta (histórico de transações paginado)
- ✅ Autenticação JWT protegendo todos os endpoints financeiros
- ✅ I/O assíncrono em toda a aplicação (FastAPI + databases)
- ✅ Documentação completa via OpenAPI/Swagger

## Stack Tecnológica

| Camada                    | Tecnologia                  |
| ------------------------- | --------------------------- |
| Framework                 | FastAPI 0.115               |
| Banco de Dados Assíncrono | databases + SQLAlchemy Core |
| Autenticação              | PyJWT (HS256)               |
| Validação                 | Pydantic v2                 |
| Migrações                 | Alembic                     |
| Runtime                   | Python 3.11+                |

## Inicializando o projeto:

### 1. Iniciar o poetry:

```bash
poetry init
```

### 2. Adicionar dependência do FastAPI

```bash
poetry add 'fastapi=*'
```

### 3. Copiar Path do Virtualenv

```bash
poetry env info
```

Ctrl + shft + p > Selecionar interpretador > Inserir caminho do interpretador > Colar caminho do path

### Testar:

- Abrir novo terminal
- Digitar "python"
- Digitar "import fastapi"

## Como Começar

```bash
# 1. Instalar dependências
poetry install

# 2. Configurar ambiente
cp .env.example .env
# Edite o .env com seus valores — especialmente JWT_SECRET

# 3. Executar migrações
alembic upgrade head

# 4. Iniciar o servidor
uvicorn src.main:app --reload
```

Documentação da API disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Estrutura do Projeto

```
src/
├── controllers/   # Rotas do FastAPI (camada HTTP)
├── models/        # Definições de tabelas com SQLAlchemy
├── schemas/       # Schemas de entrada com Pydantic
├── services/      # Lógica de negócio
├── views/         # Modelos de resposta com Pydantic
├── config.py      # Configurações via variáveis de ambiente
├── database.py    # Engine e conexão com o banco
├── exceptions.py  # Erros personalizados da aplicação
├── security.py    # Assinatura/verificação JWT e dependências de auth
└── main.py        # Fábrica da aplicação e ponto de entrada
```

## Autenticação

Todos os endpoints `/accounts` e `/transactions` exigem um token Bearer.

```bash
# 1. Obter um token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'

# 2. Usar o token
curl http://localhost:8000/accounts/?limit=10 \
  -H "Authorization: Bearer <token>"
```
