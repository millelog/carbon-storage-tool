# Carbon Storage Site Mapping Tool Backend

FastAPI backend for the Carbon Storage Site Mapping Tool.

## Quick Start

1. Create and activate a virtual environment.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the necessary variables

4. Start the development server:
   ```
   uvicorn main:app --reload
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Key Features

- GeoJSON data serving for multiple layer types
- In-memory caching for improved performance
- Integration with PostgreSQL and PostGIS

## Database Setup

Ensure PostgreSQL is installed with the PostGIS extension. Run the provided SQL scripts to set up the necessary tables and indexes.

## API Endpoints

- `/layers`: Get available layers
- `/layers/{layer_name}/geojson`: Get GeoJSON data for a specific layer
- `/layers/{layer_name}/schema`: Get schema information for a layer

## Troubleshooting

- Check application logs for errors
- Verify database connection and PostGIS setup
- Ensure all environment variables are correctly set