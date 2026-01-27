# Todo App - Full-Stack Task Management

A modern, full-stack Todo application built with Next.js and FastAPI, demonstrating professional software development practices with AI-assisted spec-driven development.

## Live Demo

- **Frontend**: [https://your-app.vercel.app](https://your-app.vercel.app) *(Update after deployment)*
- **Backend API**: [https://your-api.railway.app](https://your-api.railway.app) *(Update after deployment)*

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Task Completion**: Toggle tasks between pending and completed
- **Filtering & Sorting**: Filter by status (All/Pending/Completed), sort by date or title
- **Responsive Design**: Works beautifully on mobile, tablet, and desktop
- **Real-time Updates**: Optimistic UI updates with SWR
- **Clean UI**: Modern design with Tailwind CSS and Radix UI components

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Validation**: Pydantic

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Authentication**: Better Auth
- **Data Fetching**: SWR
- **Notifications**: Sonner

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway
- **Database**: Neon PostgreSQL
- **Local Development**: Docker Compose

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/Hackathon-2-todo-app.git
cd Hackathon-2-todo-app

# Copy environment file
cp .env.example .env
# Edit .env with your database URL and secrets

# Start all services
docker-compose up

# Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Option 2: Manual Setup

**Backend:**
```bash
cd phase-2/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd phase-2/frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

## Project Structure

```
Hackathon-2-todo-app/
├── README.md                    # This file
├── CLAUDE.md                    # AI assistant context
├── AGENTS.md                    # AI-assisted development methodology
├── DEPLOYMENT.md                # Production deployment guide
├── docker-compose.yml           # Local development setup
├── .env.example                 # Environment variables template
│
├── phase-1/                     # Console app (legacy)
│   └── src/                     # Python console application
│
├── phase-2/                     # Full-stack web app
│   ├── backend/                 # FastAPI backend
│   │   ├── src/
│   │   │   ├── main.py          # Application entry point
│   │   │   ├── config.py        # Settings management
│   │   │   ├── database.py      # Database connection
│   │   │   ├── models/          # SQLAlchemy models
│   │   │   ├── schemas/         # Pydantic schemas
│   │   │   ├── repositories/    # Data access layer
│   │   │   ├── api/             # API routes
│   │   │   └── core/            # Security, exceptions
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── .env.example
│   │
│   ├── frontend/                # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/             # Pages and routes
│   │   │   ├── components/      # React components
│   │   │   ├── lib/             # Utilities and clients
│   │   │   └── types/           # TypeScript types
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── .env.example
│   │
│   └── specs/                   # Module specifications
│       ├── 001-backend-api-database/
│       ├── 002-auth-user-management/
│       ├── 003-frontend-ui/
│       └── 004-integration-deployment/
│
├── history/prompts/             # AI conversation records
└── .specify/                    # Spec-Kit Plus configuration
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Health check | No |
| GET | `/api/tasks` | List user's tasks | Yes |
| POST | `/api/tasks` | Create a new task | Yes |
| GET | `/api/tasks/{id}` | Get task by ID | Yes |
| PUT | `/api/tasks/{id}` | Update task | Yes |
| DELETE | `/api/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/tasks/{id}/toggle` | Toggle completion | Yes |

### Request/Response Examples

**Create Task:**
```bash
curl -X POST https://your-api.railway.app/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2026-01-26T12:00:00Z",
  "updated_at": "2026-01-26T12:00:00Z"
}
```

## Environment Variables

See `.env.example` for all required variables. Key variables:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Secret for JWT signing (32+ chars) |
| `BETTER_AUTH_SECRET` | Must match JWT_SECRET |
| `NEXT_PUBLIC_API_URL` | Backend API URL |
| `CORS_ORIGINS` | Allowed frontend origins |

## Development

### Running Tests

```bash
# Backend
cd phase-2/backend
pytest

# Frontend
cd phase-2/frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd phase-2/backend
flake8 src/
mypy src/

# Frontend linting
cd phase-2/frontend
npm run lint
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
1. Push to GitHub
2. Deploy backend to Railway (set `phase-2/backend` as root)
3. Deploy frontend to Vercel (set `phase-2/frontend` as root)
4. Configure environment variables
5. Update CORS origins

## AI-Assisted Development

This project was built using **Spec-Driven Development (SDD)** with AI assistance. See [AGENTS.md](./AGENTS.md) for methodology details.

### Development Workflow
```
/sp.specify → /sp.plan → /sp.tasks → /sp.implement
```

### Modules Developed
1. **Backend API & Database**: FastAPI REST API with PostgreSQL
2. **Auth & User Management**: JWT authentication with Better Auth
3. **Frontend UI**: Next.js with Tailwind CSS
4. **Integration & Deployment**: Docker, Railway, Vercel

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework for production
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Better Auth](https://better-auth.com/) - Authentication library
- [Neon](https://neon.tech/) - Serverless PostgreSQL
- [Railway](https://railway.app/) - Backend hosting
- [Vercel](https://vercel.com/) - Frontend hosting
- [Spec-Kit Plus](https://github.com/spec-kit/spec-kit-plus) - SDD framework

---

Built with AI assistance using Claude Code and Spec-Driven Development.
