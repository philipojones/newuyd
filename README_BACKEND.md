# United Youth Developers (UYD) FastAPI Backend

This is the FastAPI backend for the United Youth Developers website, providing REST API endpoints for programs, events, news, and site statistics.

## Features

- **Programs Management**: CRUD operations for youth development programs
- **Events Management**: Event creation, retrieval, and management
- **News Articles**: Article management system
- **Site Statistics**: Dynamic site stats for the frontend
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

3. **Run the Server**:
   ```bash
   python main.py
   ```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Programs
- `GET /api/programs/` - List all programs
- `GET /api/programs/featured/` - Get featured programs
- `GET /api/programs/{id}` - Get specific program
- `POST /api/programs/` - Create new program
- `PUT /api/programs/{id}` - Update program
- `DELETE /api/programs/{id}` - Delete program

### Events
- `GET /api/events/` - List all events
- `GET /api/events/upcoming/` - Get upcoming events
- `GET /api/events/{id}` - Get specific event
- `POST /api/events/` - Create new event
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event

### News
- `GET /api/news/` - List all articles
- `GET /api/news/latest/` - Get latest news
- `GET /api/news/featured/` - Get featured articles
- `GET /api/news/{id}` - Get specific article
- `POST /api/news/` - Create new article

### Site Stats
- `GET /api/core/stats/` - Get site statistics

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


