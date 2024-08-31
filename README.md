# Carbon Storage Site Mapping Tool

An interactive web application for exploring potential carbon storage sites, built with React, ArcGIS JS API, and FastAPI.

## Quick Start

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- pnpm (v6+)
- PostgreSQL with PostGIS

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/carbon-storage-tool.git
   cd carbon-storage-tool
   ```

2. Set up the frontend:
   ```
   cd frontend
   pnpm install
   pnpm run dev
   ```

3. Set up the backend:
   ```
   cd ../backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. Open `http://localhost:5173` in your browser.

## Features

- Interactive mapping of potential carbon storage sites
- Geospatial data visualization
- Backend API for data processing and storage

## Tech Stack

- Frontend: React, TypeScript, Vite, ArcGIS JS API, shadcn UI
- Backend: FastAPI, SQLAlchemy, GeoPandas
- Database: PostgreSQL with PostGIS