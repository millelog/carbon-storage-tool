# Carbon Storage Site Mapping Tool

An interactive web application for exploring potential carbon storage sites, built with React, Leaflet, and FastAPI.

## Quick Start

### Prerequisites
- Node.js (v18+)
- Python (v3.12+)
- Docker and Docker Compose (for production deployment)
- Visual Studio Code (for development)

## Development Environment

The development environment is set up to run using Visual Studio Code's launch configurations.

1. Clone the repository:
   ```
   git clone https://github.com/your-username/carbon-storage-tool.git
   cd carbon-storage-tool
   ```

2. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add necessary environment variables (e.g., `DEV_GDB`)

3. Frontend Setup:
   - Navigate to the `frontend` directory
   - Install dependencies: `npm install`
   - Start the development server: `npm run dev`

4. Backend Setup:
   - Open the project in Visual Studio Code
   - Ensure you have the Python extension installed
   - Setup python environment: `python -m venv .venv && source .venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`
   - Use the provided `launch.json` configuration to start the backend server

5. Access the application at `http://localhost:5173` (or the port specified by Vite)

## Production Deployment

Production deployment is handled using Docker Compose.

1. Ensure Docker and Docker Compose are installed on your production server

2. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add production-specific variables (`POSTGRES_PASSWORD`)

3. Build and run with Docker Compose:
   ```
   docker-compose up --build
   ```

4. Access the application at the specified production URL

## Features

- Interactive mapping of potential carbon storage sites
- Geospatial data visualization using Leaflet
- Dynamic layer selection and rendering
- Backend API for processing geodatabase files

## Tech Stack

- Frontend: React, TypeScript, Vite, Leaflet, shadcn UI
- Backend: FastAPI, GeoPandas
- Database: PostgreSQL with PostGIS (for future implementations)
- Containerization: Docker (for production)

## Project Structure

- `frontend/`: React application code
- `backend/`: FastAPI application code
- `.vscode/launch.json`: VS Code launch configurations for development
- `docker-compose.yml`: Production deployment configuration

## Environment Variables

- Development:
  - `DEV_GDB`: Path to the development geodatabase file
  - `VITE_API_URL`: Backend API URL for development (typically http://localhost:8000)

- Production:
  - `PROD_GDB`: Path to the production geodatabase file
  - `POSTGRES_PASSWORD`: Database password for production
  - `VITE_API_URL`: Backend API URL for production

## Troubleshooting

- For development issues, check VS Code's Debug Console and terminal output
- For production, review Docker Compose logs: `docker-compose logs`
- Ensure all required environment variables are set correctly for each environment
- Verify that the geodatabase file paths are correct for your environment

For more detailed information, refer to the documentation in the `docs` directory.