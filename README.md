# 🍽️ BitePlate — Smart Restaurant Management System

**Unit 27: Advanced Programming | BTEC Level 5 HN | Y/615/1651**

Full-stack restaurant management system: **Django + FastAPI** backend + **React + Vite** frontend, containerised with Docker Compose.

---

## Quick Start — 3 commands

```bash
git clone https://github.com/<you>/biteplate.git && cd biteplate
cp .env.example .env
docker compose up --build
```

| Service | URL |
|---|---|
| **Frontend (React)** | http://localhost:5173 |
| **API (FastAPI)** | http://localhost:8000/api |
| **Swagger Docs** | http://localhost:8000/api/docs |
| **Django Admin** | http://localhost:8000/admin |

---

## Local Dev (no Docker)

### Backend
```bash
# 1. Virtual env
python -m venv .venv && source .venv/bin/activate

# 2. Install
pip install -r requirements.txt

# 3. Run (SQLite, no Postgres needed)
cd src
DJANGO_SETTINGS_MODULE=core.settings.development python manage.py migrate
DJANGO_SETTINGS_MODULE=core.settings.development python manage.py loaddata fixtures/initial_data.json
DJANGO_SETTINGS_MODULE=core.settings.development uvicorn core.asgi:application --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env        # VITE_API_URL=http://localhost:8000/api
npm run dev                  # → http://localhost:5173
```

---

## Environment Variables (.env)

Copy `.env.example` to `.env`. Required variables:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | *(set this!)* | Django secret key |
| `DB_NAME` | `biteplate` | Postgres database name |
| `DB_USER` | `biteplate_user` | Postgres user |
| `DB_PASSWORD` | `biteplate_pass` | Postgres password |
| `DB_HOST` | `db` | Hostname (use `db` in Docker) |
| `REDIS_URL` | `redis://redis:6379/0` | Redis URL |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Celery broker |
| `DEFAULT_TAX_RATE` | `0.12` | Tax rate (12%) |
| `CORS_ORIGINS` | `http://localhost:5173` | Allowed frontend origins |

---

## Docker Services

```
docker compose up --build
```

| Container | Role |
|---|---|
| `backend` | Django + FastAPI (ASGI via uvicorn) |
| `frontend` | React build served by nginx (proxies `/api` → backend) |
| `db` | PostgreSQL 16 |
| `redis` | Redis 7 (cache + Celery broker) |
| `worker` | Celery async worker |
| `beat` | Celery Beat (scheduled tasks) |

### First-time setup (after `docker compose up`):
```bash
# Create admin user
docker compose exec backend python manage.py createsuperuser
```

---

## Design Patterns (6 Patterns)

| # | Pattern | Where | Purpose |
|---|---|---|---|
| 1 | **Command** | `apps/kitchen/commands.py` | Kitchen actions with undo |
| 2 | **Observer** | `apps/orders/observers.py` | Notify Waiter/Kitchen/Manager on status change |
| 3 | **Strategy** | `core/patterns/strategy.py` | Swap pricing at runtime |
| 4 | **Factory Method** | `apps/menu/factories.py` | Create menu items by category |
| 5 | **Decorator** | `core/patterns/decorator.py` | Runtime dish customisation |
| 6 | **Singleton** | `apps/orders/history.py` | Global order history log |

---

## Project Structure

```
biteplate/
├── src/                        # Django + FastAPI backend
│   ├── apps/
│   │   ├── tables/             # Table state machine
│   │   ├── reservations/       # Bookings + Celery reminders
│   │   ├── orders/             # Orders (Observer Subject)
│   │   ├── kitchen/            # Kitchen queue (Command pattern)
│   │   ├── menu/               # Menu (Factory + Decorator)
│   │   ├── billing/            # Billing (Strategy + Facade)
│   │   └── staff/              # RBAC user model
│   ├── core/
│   │   ├── patterns/           # Abstract base classes (all 6 patterns)
│   │   └── settings/           # base / development / production
│   └── infrastructure/
│       └── celery_app/         # Async tasks
├── frontend/                   # React + Vite + TailwindCSS
│   ├── src/
│   │   ├── pages/              # Dashboard, Tables, Orders, Kitchen, Menu, Billing
│   │   ├── components/         # Layout, UI components
│   │   └── services/           # Axios API client + mock data
│   └── nginx.conf              # Serves SPA + proxies /api
├── docs/
│   ├── diagrams/               # 5 PNG diagrams
│   └── ARCHITECTURE.md         # Patterns documented with code
├── tests/
│   └── test_patterns.py        # 17 unit tests (all pass)
├── Dockerfile                  # Backend image
├── docker-compose.yml          # Full stack
├── requirements.txt
└── .env.example
```

---

## Tests

```bash
# Backend unit tests (17 tests)
cd biteplate
DJANGO_SETTINGS_MODULE=core.settings.development python -m pytest tests/ -v

# With coverage
coverage run -m pytest tests/
coverage report
```

---

## API Endpoints

Full interactive docs at **http://localhost:8000/api/docs**

```
GET    /api/tables/                      List all tables
POST   /api/tables/{id}/seat             Seat guests
POST   /api/orders/                      Create order
POST   /api/orders/{id}/confirm          Confirm → triggers kitchen
GET    /api/kitchen/queue                Kitchen ticket queue
POST   /api/kitchen/tickets/{id}/ready   Mark item ready
POST   /api/billing/generate/{order_id}  Generate bill
GET    /api/menu/items                   List menu items
POST   /api/reservations/               Create reservation
```

---

## Celery Tasks

| Task | Trigger | Purpose |
|---|---|---|
| `notify_kitchen_on_order` | Order confirmed | Create KitchenTickets |
| `send_reservation_reminder` | 2h before booking | SMS to customer |
| `broadcast_order_status` | Status change | WebSocket push |
| `generate_end_of_night_report` | Daily 23:59 | Revenue report |

---

*BitePlate · Unit 27 Advanced Programming · BTEC Level 5 · Y/615/1651*
