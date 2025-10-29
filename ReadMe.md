# TO DO LIST APP — Backend

## Project Overview

TO DO LIST APP is a simple backend API built with FastAPI that provides the core CRUD operations for managing todo items. It's intended for developers who need a lightweight, production-ready REST backend for a todo-style application, demos, or as a learning example for FastAPI + SQLAlchemy + PostgreSQL development. The service stores todos in a PostgreSQL database and exposes endpoints to create, read, update, and delete tasks.

## Key Features

- ⚙️ CRUD endpoints for todo items (create, read, update, delete)
- ✅ Pydantic validation for request and response models
- 🗄️ Persistent storage using PostgreSQL via SQLAlchemy
- 🐳 Docker and docker-compose support for easy local development
- 🔁 Automatic database table creation on startup
- 🌐 Configurable CORS origins

## Tech Stack

- **Language:** Python 3.13.4
- **Web Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Database:** PostgreSQL
- **Containerization:** Docker, docker-compose
- **Testing:** pytest (tests present/placeholder)
- **ASGI Server:** Uvicorn

## Project Structure

```
.
├── Dockerfile                      # Docker image for the backend
├── docker-compose.yml              # Compose config (Postgres + app)
├── requirements.txt                # Python dependencies
├── todo-backend.postman_collection.json
├── app/
│   ├── main.py                     # FastAPI app, startup lifecycle, include routers
│   ├── db.py                       # SQLAlchemy engine/session, Base, DB helpers
│   ├── models.py                   # SQLAlchemy models (Todo)
│   ├── schemas.py                  # Pydantic schemas for request/response
│   └── core/
│       └── cors.py                 # CORS setup helper
│   └── routers/
│       └── todos.py                # Todos router: GET, POST, PATCH, DELETE
├── tests/
│   └── test_todos.py               # (Placeholder) tests for the todos endpoints
```

**File notes:**
- `app/main.py` — creates the FastAPI `app`, sets up CORS and lifecycle handler that calls `create_db_and_tables()` on startup.
- `app/db.py` — defines `DATABASE_URL`, SQLAlchemy `engine`, `SessionLocal`, `Base`, `create_db_and_tables()`, and `get_db()` dependency.
- `app/models.py` — defines the `Todo` SQLAlchemy model and the database table `todos`.
- `app/schemas.py` — Pydantic models: `TodoCreate`, `TodoUpdate`, `Todo` (response).
- `app/routers/todos.py` — REST endpoints for /todos.

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd Todo-backend
```

### 2. Create a Python virtual environment and activate it (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

See the next section for details on environment variables.

## Environment Variables

The app reads environment variables to configure database and CORS. Create a `.env` file in the project root (or export env vars in your shell).

**Example `.env` file:**

```env
# PostgreSQL URL format:
# postgresql://<username>:<password>@<host>:<port>/<database>
DATABASE_URL=postgresql://postgres:1234@localhost:5432/tododb

# CORS origins (comma-separated). Default: http://localhost:5173
CORS_ORIGINS=http://localhost:5173
```

**Notes:**
- If `DATABASE_URL` is not provided, the code falls back to `postgresql://postgres:1234@localhost:5432/tododb`.
- The app creates missing tables automatically on startup via `create_db_and_tables()`.

## Running the Application

### Local (development)

Start the API with Uvicorn (dev, auto-reload):

```bash
uvicorn app.main:app --reload
```

- The API will be available at: **http://127.0.0.1:8000**
- Open the interactive docs at: **http://127.0.0.1:8000/docs**

The FastAPI `lifespan` handler will call `create_db_and_tables()` at startup to create tables.

### Docker (recommended for matching production)

**1. Build and run with docker-compose:**

```bash
docker-compose up --build
```

This assumes `docker-compose.yml` launches both the PostgreSQL service and the backend service. The backend uses `DATABASE_URL` to connect to the DB.

**2. Stop and remove containers:**

```bash
docker-compose down
```

## Database Details

- **Default connection string:** `postgresql://postgres:1234@localhost:5432/tododb`
- **Table:** `todos`
- **Schema** (SQLAlchemy model in `app/models.py`):
  - `id` — integer, primary key, indexed
  - `title` — string(140), not nullable, indexed
  - `done` — boolean, not nullable, default False

The application uses SQLAlchemy Core + ORM:
- `engine = create_engine(DATABASE_URL)`
- `SessionLocal = sessionmaker(...)`
- `Base = declarative_base()`
- `create_db_and_tables()` calls `Base.metadata.create_all(bind=engine)` to ensure tables exist.

## API Endpoints

**Base path:** `/todos`

### 1. Get all todos

- **Method:** `GET`
- **Route:** `/todos/`
- **Description:** Retrieve a list of todos with optional pagination (skip, limit).
- **Query params:**
  - `skip` (int, default 0)
  - `limit` (int, default 100)
- **Response:** 200 OK — JSON array of Todo objects

**Sample curl:**
```bash
curl -sS "http://127.0.0.1:8000/todos/?skip=0&limit=100"
```

**Sample response:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "done": false
  },
  {
    "id": 2,
    "title": "Write report",
    "done": true
  }
]
```

### 2. Create a new todo

- **Method:** `POST`
- **Route:** `/todos/`
- **Description:** Create a todo. `title` is required (1-140 chars).
- **Body (application/json):**
```json
{
  "title": "New task title"
}
```
- **Response:** 201 Created — JSON of created Todo (includes `id`)

**Sample curl:**
```bash
curl -X POST "http://127.0.0.1:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Finish homework"}'
```

### 3. Update a todo

- **Method:** `PATCH`
- **Route:** `/todos/{id}`
- **Description:** Update `title` and/or `done` for the todo with given ID. Patch accepts partial data.
- **Body example:**
```json
{
  "title": "Updated title",
  "done": true
}
```
- **Response:** 200 OK — JSON of updated Todo
- **Error:** 404 if todo not found

### 4. Delete a todo

- **Method:** `DELETE`
- **Route:** `/todos/{id}`
- **Description:** Delete the todo with the given ID.
- **Response:** 204 No Content on success
- **Error:** 404 if todo not found

**API docs (interactive):** `http://127.0.0.1:8000/docs`

## Frontend Integration

(Backend repo — notes for frontend developers)

- Set your frontend API base URL to point to the backend host, for example:
  - Vite: `VITE_API_URL=http://127.0.0.1:8000`
- Ensure `CORS_ORIGINS` includes the frontend origin (e.g., `http://localhost:5173`) so the browser can call the backend.
- **Typical flow:**
  - GET `/todos/` to fetch list
  - POST `/todos/` to create
  - PATCH `/todos/{id}` to modify
  - DELETE `/todos/{id}` to remove