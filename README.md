# RadiantOJ ⚡

A production-grade Online Judge built from scratch — supporting Python, C, and C++ code execution with async judging, JWT authentication, Redis caching, and full Docker deployment on AWS EC2.

**Live:** http://13.233.96.29

---

## Tech Stack

**Backend:** Django, Django REST Framework, PostgreSQL, Redis, Celery, JWT (SimpleJWT)

**Frontend:** React (Vite), Tailwind CSS, Axios, Monaco Editor

**DevOps:** Docker Compose, AWS EC2, Nginx, GitHub Actions (CI/CD)

---

## Features

- **Authentication** — Register, Login, Logout with JWT access/refresh tokens and token blacklisting
- **Problems** — List with pagination and difficulty filtering, detail view, admin-only create/update/delete
- **Code Editor** — Monaco Editor (VS Code) with Python, C++, C support
- **Run Code** — Execute code with custom input, get instant output
- **Submit Code** — Async judging via Celery — ACCEPTED, WRONG_ANSWER, TLE, RE, CE verdicts
- **Submissions** — Per-problem and all-submissions history
- **Redis Caching** — Problems list cached with auto-invalidation on create
- **RBAC** — Admin-only problem management, authenticated users for submissions
- **CI/CD** — Auto deploy to EC2 on every push to `dev` branch

---

## System Architecture

```
Browser
  │
  ├── GET /          → Nginx → React (dist/)
  └── POST /auth/    → Nginx → Django (port 8000)
                                  │
                          ┌───────┴────────┐
                          │                │
                     PostgreSQL          Redis
                     (data store)     (cache + queue)
                                          │
                                       Celery
                                    (judge worker)
```

---

## API Reference

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register/` | Register new user | No |
| POST | `/auth/login/` | Login → JWT tokens | No |
| POST | `/auth/logout/` | Logout (blacklist token) | Yes |
| GET | `/problems/` | List problems (paginated) | Yes |
| POST | `/problems/` | Create problem | Admin |
| GET | `/problems/<id>/` | Problem detail | Yes |
| POST | `/submissions/problem/<id>/` | Submit code | Yes |
| GET | `/submissions/problem/<id>/` | Problem submissions | Yes |
| GET | `/submissions/` | All user submissions | Yes |
| POST | `/judge/run/` | Run code with custom input | Yes |

---

## Local Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL
- Redis
- Docker (optional)

### Without Docker

```bash
# Clone
git clone https://github.com/ANKISH1/RadiantOJ.git
cd RadiantOJ

# Backend
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # fill in your values

python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Celery (new terminal)
cd backend
celery -A core worker --loglevel=info
```

### With Docker

```bash
# Clone
git clone https://github.com/ANKISH1/RadiantOJ.git
cd RadiantOJ

# Create .env.docker (see Environment Variables below)

# Build and run
docker-compose up --build
```

Visit: http://localhost:8000

---

## Environment Variables

Create `.env.docker` in root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=radiantoj
DB_USER=radiantoj_user
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
REDIS_URL=redis://redis:6379/1
```

---

## Project Structure

```
RadiantOJ/
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD — auto deploy on dev push
├── Dockerfile
├── docker-compose.yml
├── backend/
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── celery.py
│   └── apps/
│       ├── users/            # Auth — custom User model
│       ├── problems/         # Problems + TestCases
│       ├── submissions/      # Submission tracking
│       └── judge/            # Code execution (Run + Submit)
└── frontend/
    └── src/
        ├── api/axios.js      # Axios instance + interceptors
        ├── pages/            # Login, Register, Problems, ProblemDetail, Submissions
        └── components/       # Navbar, ProtectedRoute
```

---

## Git Workflow

```
main     ← stable production
  └── dev    ← development + CI/CD trigger
        └── feature/*    ← individual features
```

Every push to `dev` → GitHub Actions → SSH into EC2 → `git pull` + `npm run build` + `docker-compose up --build`

---

## Deployment (AWS EC2)

- **Instance:** t2.micro (Ubuntu 24.04)
- **Web Server:** Nginx (port 80 → React, proxy → Django)
- **Containers:** Docker Compose (web, db, redis, celery)
- **CI/CD:** GitHub Actions with SSH deploy

---

## Author

**Ankish Chaudhary**  
B.Tech CS — UPES | Ex-TCS | AlgoUniversity Externship  
Dharamshala, HP