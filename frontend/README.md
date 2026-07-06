# BitePlate Frontend

React + Vite + TailwindCSS dashboard for the BitePlate Smart Restaurant Management System.

## Pages

| Page | Route | Description |
|---|---|---|
| Dashboard | `/` | Revenue charts, active orders, kitchen overview |
| Tables | `/tables` | Visual table grid with state transitions |
| Orders | `/orders` | Create, confirm, cancel orders |
| Kitchen | `/kitchen` | Kanban queue — Command pattern with undo |
| Menu | `/menu` | Menu item management with Decorator preview |
| Billing | `/billing` | Bill generation — Strategy pattern selector |

## Quick Start

```bash
npm install
cp .env.example .env
npm run dev
# Opens at http://localhost:5173
```

## Connect to Backend

In `.env`:
```
VITE_API_URL=http://localhost:8000/api
```

The app runs with **mock data** out of the box. When the backend is running, all API calls in `src/services/api.js` will be used.

## Build for Production

```bash
npm run build
# Output in dist/
```

## Tech Stack

- **React 18** — UI
- **React Router v6** — routing
- **TailwindCSS** — styling
- **Recharts** — charts (Dashboard)
- **Zustand** — state management (ready to use)
- **Axios** — HTTP client
- **Lucide React** — icons
