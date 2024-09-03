# Carbon Storage Site Mapping Tool

An interactive web application for exploring potential carbon storage sites, built with React, Leaflet, and FastAPI.

## Quick Start

### Prerequisites
- Node.js (v18+)
- Python (v3.12+)
- PostgreSQL with PostGIS extension
- Docker and Docker Compose (for production deployment)
- Visual Studio Code (for development)

## Development Environment

1. Clone the repository and navigate to the project directory.

2. Set up environment variables:
   - Copy `.env.example` to `.env` in both `frontend` and `backend` directories
   - Fill in the necessary variables in each `.env` file

3. Frontend Setup:
   - Navigate to the `frontend` directory
   - Install dependencies: `npm install`
   - Start the development server: `npm run dev`

4. Backend Setup:
   - Navigate to the `backend` directory
   - Create and activate a virtual environment
   - Install dependencies: `pip install -r requirements.txt`
   - Start the backend server: `uvicorn main:app --reload`

5. Access the application at `http://localhost:5173`

## Production Deployment

1. Ensure Docker and Docker Compose are installed on your production server.

2. Set up environment variables:
   - Update `.env` files in `frontend` and `backend` directories with production values
   - Ensure `POSTGRES_PASSWORD` is set in the frontend's deployment environment

3. Build and run with Docker Compose:
   ```
   docker-compose up --build
   ```

## New Features

- In-memory caching for improved performance
- Support for multiple geometry types (Point, LineString, Polygon)
- Layer-specific styling in the frontend
- Detailed property information display for each feature

## Project Structure

- `frontend/`: React application with Leaflet integration
- `backend/`: FastAPI application with PostgreSQL and PostGIS
- `docker-compose.yml`: Production deployment configuration

## Environment Variables

Refer to `.env.example` files in `frontend` and `backend` directories for required variables.

## Troubleshooting

- Check application logs for errors
- Verify database connections and PostGIS setup
- Ensure all environment variables are correctly set

For more detailed information, refer to the README files in the `frontend` and `backend` directories.