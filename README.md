# Colmeia Urbana API

API REST em **FastAPI** para gestão de **apiários urbanos**: cadastro de colmeias, revisões de campo, colheitas de mel e indicadores do painel.

Este repositório é a **segunda componente** do MVP. A interface (componente principal) consome estas rotas e também consulta o **Open-Meteo** para o clima de cada ponto.

## Arquitetura

O sistema segue o **Cenário 1**: interface, API própria com persistência e um serviço externo.

![Arquitetura da Colmeia Urbana](docs/architecture.svg)

- **Interface (Front-End):** React, chama esta API via REST.
- **API (Back-End):** este serviço, com SQLite.
- **API externa:** [Open-Meteo](https://open-meteo.com/), consumida pela interface.

## Funcionalidades extras (além do CRUD)

- Autenticação JWT
- Busca, filtro por situação, ordenação e paginação de colmeias
- Índice de saúde da colmeia a partir da última revisão
- Painel agregado com produção mensal de mel

## Rotas principais

Documentação interativa no Swagger: `http://localhost:8000/docs`

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Cria conta e devolve token |
| `POST` | `/api/auth/login` | Autentica (`username` = e-mail) |
| `GET` | `/api/auth/me` | Usuário autenticado |
| `GET` | `/api/hives` | Lista colmeias com filtros e paginação |
| `POST` | `/api/hives` | Cadastra colmeia |
| `GET` | `/api/hives/{id}` | Detalha colmeia |
| `PUT` | `/api/hives/{id}` | Atualiza colmeia |
| `DELETE` | `/api/hives/{id}` | Remove colmeia |
| `GET` | `/api/inspections` | Lista revisões |
| `POST` | `/api/inspections` | Registra revisão |
| `PUT` | `/api/inspections/{id}` | Atualiza revisão |
| `DELETE` | `/api/inspections/{id}` | Remove revisão |
| `GET` | `/api/harvests` | Lista colheitas |
| `POST` | `/api/harvests` | Registra colheita |
| `DELETE` | `/api/harvests/{id}` | Remove colheita |
| `GET` | `/api/dashboard/summary` | Indicadores do painel |

Conta de demonstração criada na primeira execução:

- **E-mail:** `apicultor@colmeia.dev`
- **Senha:** `colmeia123`

No Swagger, use **Authorize** com o e-mail no campo `username`.

## Instalação local

1. Instale o **Python 3.12**.
2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicie a API:

```bash
uvicorn app.main:app --reload --port 8000
```

5. O Swagger abre sozinho no navegador padrão em `http://127.0.0.1:8000/docs`.

Para não abrir o navegador, inicie com `COLMEIA_OPEN_BROWSER=0`.

O banco SQLite é criado automaticamente em `data/colmeia.db`.

## Execução com Docker

Na raiz deste repositório:

```bash
docker build -t colmeia-api .
docker run --rm -p 8000:8000 -v colmeia_data:/app/data colmeia-api
```

A documentação fica em `http://localhost:8000/docs`.

O `docker-compose` do sistema completo está na raiz do repositório da **interface** (`colmeia-web`), como exigido para a componente principal.

## Estrutura

```text
colmeia-api/
├── Dockerfile
├── README.md
├── requirements.txt
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── seed.py
│   └── routers/
└── docs/
    └── architecture.svg
```
