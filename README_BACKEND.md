# United Youth Developers (UYD) Full-Stack Server

This is the complete FastAPI server for the United Youth Developers website, providing both the website frontend (HTML templates) and REST API backend on the same port.

## Features

- **Website Frontend**: HTML templates served via Jinja2
- **REST API**: CRUD operations for programs, events, news, and site statistics
- **Static Files**: CSS, JS, and images served automatically
- **SQLite Database**: Lightweight database for development and small-scale deployment
- **CORS Support**: Configured for frontend integration

## Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Seed the Database** (optional):

   ```bash
   python seed_data.py
   ```

3. **Configure API Key Security**:

   Create a `.env` file (or update the existing one) and define a key that will be required on every `POST`, `PUT`, and `DELETE` request:

   ```bash
   echo "UYD_API_KEY=super-secret-key" >> .env
   ```

   When calling protected endpoints, include the header `X-API-Key: super-secret-key`. If the header is missing or incorrect, the request will be rejected.

4. **Run the Server**:

   ```bash
   # Easy startup
   python run.py

   # Or directly with uvicorn
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The website and API will be available at `http://localhost:8000`

## Available Routes

### Website Pages

- `GET /` - Home page
- `GET /about` - About Us page
- `GET /programs` - Programs page
- `GET /events` - Events page
- `GET /contact` - Contact page
- `GET /get-involved` - Get Involved page
- `GET /news` - News page
- And more...

### API Endpoints

#### Programs

- `GET /api/programs` - List all programs
- `GET /api/programs/featured` - Get featured programs
- `GET /api/programs/{id}` - Get specific program
- `POST /api/programs` - Create new program *(requires `X-API-Key` header)*
- `PUT /api/programs/{id}` - Update program
- `DELETE /api/programs/{id}` - Delete program

#### Events

- `GET /api/events` - List all events
- `GET /api/events/upcoming` - Get upcoming events
- `GET /api/events/{id}` - Get specific event
- `POST /api/events` - Create new event *(requires `X-API-Key` header)*
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event

#### News

- `GET /api/news` - List all articles
- `GET /api/news/latest` - Get latest news
- `GET /api/news/featured` - Get featured articles
- `GET /api/news/{id}` - Get specific article
- `POST /api/news` - Create new article *(requires `X-API-Key` header)*

#### Site Stats

- `GET /api/core/stats` - Get site statistics

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

## Database Schema

The application uses SQLite with the following main tables:

- `programs`: Youth development programs
- `events`: Events and activities
- `news_articles`: News and blog articles

## Development

To modify the database schema, update the SQLAlchemy models in `main.py` and recreate the database.

For production deployment, consider:

- Using PostgreSQL instead of SQLite
- Adding authentication/authorization
- Implementing proper logging
- Adding rate limiting
- Setting up proper CORS configuration
