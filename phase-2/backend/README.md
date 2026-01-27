# Todo Backend API

FastAPI backend for the Todo application with Neon PostgreSQL database.

## Prerequisites

- Python 3.13+
- Neon PostgreSQL account (https://neon.tech)

## Quick Start

1. **Create virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your DATABASE_URL from Neon
   # Set JWT_SECRET to match your frontend BETTER_AUTH_SECRET
   ```

4. **Start server**

   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

5. **View API docs**

   Open http://localhost:8000/docs

## API Endpoints

All task endpoints require JWT authentication (Module 2).

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | / | Health check | No |
| GET | /api/{user_id}/tasks | List all tasks | Yes |
| POST | /api/{user_id}/tasks | Create a task | Yes |
| GET | /api/{user_id}/tasks/{id} | Get single task | Yes |
| PUT | /api/{user_id}/tasks/{id} | Update a task | Yes |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion | Yes |
| DELETE | /api/{user_id}/tasks/{id} | Delete a task | Yes |

## Authentication

### JWT Token Format

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Token Claims

The JWT token must contain:

| Claim | Type | Description |
|-------|------|-------------|
| `sub` | UUID | User ID |
| `email` | string | User's email |
| `name` | string | User's display name |
| `iat` | integer | Issued at timestamp |
| `exp` | integer | Expiration timestamp |

### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 401 | NOT_AUTHENTICATED | Missing Authorization header |
| 401 | INVALID_TOKEN | Malformed or invalid signature |
| 401 | TOKEN_EXPIRED | Token has expired |
| 403 | ACCESS_DENIED | User cannot access this resource |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection string |
| API_PORT | No | 8000 | Server port |
| API_HOST | No | 0.0.0.0 | Server host |
| CORS_ORIGINS | No | localhost:3000 | Allowed CORS origins |
| ENVIRONMENT | No | development | Environment mode |
| LOG_LEVEL | No | INFO | Logging level |
| JWT_SECRET | Yes | - | JWT signing secret (match BETTER_AUTH_SECRET) |
| JWT_ALGORITHM | No | HS256 | JWT algorithm |
| JWT_EXPIRATION_DAYS | No | 7 | Token expiration in days |

## Project Structure

```
phase-2/backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models/              # SQLModel entities
│   │   ├── task.py         # Task model
│   │   └── user.py         # User model (Module 2)
│   ├── schemas/             # Pydantic request/response models
│   │   ├── task.py         # Task schemas
│   │   └── auth.py         # Auth schemas (Module 2)
│   ├── repositories/        # Data access layer
│   │   ├── task_repository.py
│   │   └── user_repository.py (Module 2)
│   ├── api/                 # API routes
│   │   ├── routes/         # Route handlers
│   │   ├── middleware/     # JWT middleware (Module 2)
│   │   └── dependencies.py # DI setup
│   └── core/                # Core utilities
│       ├── exceptions.py   # Custom exceptions
│       ├── security.py     # JWT verification (Module 2)
│       └── logging_config.py
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
