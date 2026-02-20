# StreamStock 📦

StreamStock is a production-quality reference implementation for the **Python Stream Processing Framework (PSPF)**. It demonstrates how to build a scalable, event-driven inventory management system using PSPF, FastAPI, React, and PostgreSQL.

## 🏗️ Architecture

StreamStock follows an **Event-Sourcing-Lite** architecture:
- **Event Bus**: Redis Streams via PSPF.
- **Backend**: FastAPI (API) + Independent PSPF Processors (Workers).
- **Frontend**: React + Vite + TailwindCSS.
- **Storage**: PostgreSQL (Read Model) + Redis (Stream Store/Cache).

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local logic dev)
- Node.js 18+ (for frontend dev)

### Run with Docker Compose

1. **Start the stack:**
   ```bash
   docker-compose up --build
   ```
   
2. **Access the services:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redis Commander (if added) or connect to Redis on port 6379.

## 📂 Project Structure

- `backend/` - FastAPI app and PSPF Processors.
    - `api/` - REST endpoints and Websockets.
    - `streams/` - PSPF Client and Event Schemas.
    - `processors/` - Business logic pipelines.
    - `models/` - SQLAlchemy models.
- `frontend/` - React application.
- `scripts/` - Utility scripts (data generation, testing).

## 🧪 Development

### Backend
All backend code is in `backend/`. 
To run verification scripts locally, ensure you have dependencies installed (or use the docker container).

### Frontend
Frontend code is in `frontend/`. 
To run locally:
```bash
cd frontend
npm install
npm run dev
```
