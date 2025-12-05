"""API routes."""

from datetime import datetime
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.app.database.config import get_db
from src.app.database.tables import Event, NewsArticle, Program
from src.app.schemas import (
    EventResponse,
    NewsArticleCreate,
    NewsArticleResponse,
    ProgramResponse,
)
from src.app.utils.api_security import verify_api_key
from src.app.utils.image_upload import get_upload_directory, save_upload_file

base_dir = Path(__file__).parent.parent

# Database setup
DATABASE_URL = "sqlite:///./uyd.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

router = APIRouter()


@router.post("/api/programs")
async def create_program(
    title: str,
    description: str,
    content: str,
    is_featured: bool = False,
    category: Literal["Tech", "Arts", "Sports", "Others"] = "Others",
    featured_image_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> ProgramResponse:
    """Create a new program with optional image upload."""
    # Handle image upload if provided
    featured_image_path = None
    if featured_image_file:
        upload_dir = get_upload_directory()
        featured_image_path = await save_upload_file(featured_image_file, upload_dir)

    # Create program data
    program_data = {
        "title": title,
        "description": description,
        "category": category,
        "content": content,
        "is_featured": is_featured,
        "featured_image": featured_image_path,
    }

    db_program = Program(**program_data)
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


@router.get("/api/programs", response_model=list[ProgramResponse])
async def get_programs(
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    featured: bool | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Program).filter(Program.is_active)

    if category:
        query = query.filter(Program.category == category)
    if featured is not None:
        query = query.filter(Program.is_featured == featured)

    programs = query.offset(skip).limit(limit).all()
    return programs


@router.get("/api/programs/featured", response_model=list[ProgramResponse])
async def get_featured_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).filter(Program.is_active, Program.is_featured).all()
    return programs


@router.get("/api/programs/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: int, db: Session = Depends(get_db)):
    program = (
        db.query(Program).filter(Program.id == program_id, Program.is_active).first()
    )
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@router.put("/api/programs/{program_id}")
async def update_program(
    program_id: int,
    title: str | None = None,
    description: str | None = None,
    category: str | None = None,
    content: str | None = None,
    is_featured: bool | None = None,
    featured_image_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
) -> ProgramResponse:
    """Update an existing program with optional image upload."""
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    # Handle image upload if provided
    if featured_image_file:
        upload_dir = get_upload_directory()
        featured_image_path = await save_upload_file(featured_image_file, upload_dir)
        db_program.featured_image = featured_image_path

    # Update other fields if provided
    if title is not None:
        db_program.title = title
    if description is not None:
        db_program.description = description
    if category is not None:
        db_program.category = category
    if content is not None:
        db_program.content = content
    if is_featured is not None:
        db_program.is_featured = is_featured

    db.commit()
    db.refresh(db_program)
    return db_program


@router.delete("/api/programs/{program_id}")
async def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    db_program.is_active = False
    db.commit()
    return {"message": "Program deleted successfully"}


# Events API endpoints
@router.post("/api/events")
async def create_event(
    title: str,
    description: str,
    event_type: str,
    start_date: datetime,
    location: str,
    end_date: datetime | None = None,
    max_participants: int | None = None,
    content: str | None = None,
    registration_deadline: datetime | None = None,
    is_featured: bool = False,
    featured_image_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
) -> EventResponse:
    """Create a new event with optional image upload."""
    # Handle image upload if provided
    featured_image_path = None
    if featured_image_file:
        upload_dir = get_upload_directory()
        featured_image_path = await save_upload_file(featured_image_file, upload_dir)

    # Create event data
    event_data = {
        "title": title,
        "description": description,
        "event_type": event_type,
        "start_date": start_date,
        "location": location,
        "end_date": end_date,
        "max_participants": max_participants,
        "content": content,
        "registration_deadline": registration_deadline,
        "is_featured": is_featured,
        "featured_image": featured_image_path,
    }

    db_event = Event(**event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/api/events", response_model=list[EventResponse])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    event_type: str | None = None,
    featured: bool | None = None,
    upcoming: bool | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Event).filter(Event.is_active)

    if event_type:
        query = query.filter(Event.event_type == event_type)
    if featured is not None:
        query = query.filter(Event.is_featured == featured)
    if upcoming:
        query = query.filter(Event.start_date >= datetime.utcnow())

    events = query.order_by(Event.start_date).offset(skip).limit(limit).all()
    return events


@router.get("/api/events/upcoming", response_model=list[EventResponse])
async def get_upcoming_events(db: Session = Depends(get_db)):
    events = (
        db.query(Event)
        .filter(Event.is_active, Event.start_date >= datetime.utcnow())
        .order_by(Event.start_date)
        .limit(10)
        .all()
    )
    return events


@router.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id, Event.is_active).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/api/events/{event_id}")
async def update_event(
    event_id: int,
    title: str | None = None,
    description: str | None = None,
    event_type: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    location: str | None = None,
    max_participants: int | None = None,
    content: str | None = None,
    registration_deadline: datetime | None = None,
    is_featured: bool | None = None,
    featured_image_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
) -> EventResponse:
    """Update an existing event with optional image upload."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Handle image upload if provided
    if featured_image_file:
        upload_dir = get_upload_directory()
        featured_image_path = await save_upload_file(featured_image_file, upload_dir)
        db_event.featured_image = featured_image_path

    # Update other fields if provided
    if title is not None:
        db_event.title = title
    if description is not None:
        db_event.description = description
    if event_type is not None:
        db_event.event_type = event_type
    if start_date is not None:
        db_event.start_date = start_date
    if end_date is not None:
        db_event.end_date = end_date
    if location is not None:
        db_event.location = location
    if max_participants is not None:
        db_event.max_participants = max_participants
    if content is not None:
        db_event.content = content
    if registration_deadline is not None:
        db_event.registration_deadline = registration_deadline
    if is_featured is not None:
        db_event.is_featured = is_featured

    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/api/events/{event_id}")
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db_event.is_active = False
    db.commit()
    return {"message": "Event deleted successfully"}


# News API endpoints
@router.post("/api/news", response_model=NewsArticleResponse)
async def create_news_article(
    article: NewsArticleCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    db_article = NewsArticle(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.get("/api/news", response_model=list[NewsArticleResponse])
async def get_news(
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    featured: bool | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(NewsArticle).filter(NewsArticle.is_active)

    if category:
        query = query.filter(NewsArticle.category == category)
    if featured is not None:
        query = query.filter(NewsArticle.is_featured == featured)

    news = (
        query.order_by(NewsArticle.publish_date.desc()).offset(skip).limit(limit).all()
    )
    return news


@router.get("/api/news/latest", response_model=list[NewsArticleResponse])
async def get_latest_news(db: Session = Depends(get_db)):
    news = (
        db.query(NewsArticle)
        .filter(NewsArticle.is_active)
        .order_by(NewsArticle.publish_date.desc())
        .limit(10)
        .all()
    )
    return news


@router.get("/api/news/featured", response_model=list[NewsArticleResponse])
async def get_featured_news(db: Session = Depends(get_db)):
    news = (
        db.query(NewsArticle)
        .filter(NewsArticle.is_active, NewsArticle.is_featured)
        .order_by(NewsArticle.publish_date.desc())
        .limit(5)
        .all()
    )
    return news


@router.get("/api/news/{article_id}", response_model=NewsArticleResponse)
async def get_news_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(NewsArticle)
        .filter(NewsArticle.id == article_id, NewsArticle.is_active)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# Site stats endpoint
@router.get("/api/core/stats")
async def get_site_stats(db: Session = Depends(get_db)):
    programs_count = db.query(Program).filter(Program.is_active).count()
    events_count = db.query(Event).filter(Event.is_active).count()
    news_count = db.query(NewsArticle).filter(NewsArticle.is_active).count()

    # Mock subscriber count - in real app, you'd have a subscribers table
    subscribers_count = 1250

    return {
        "programs": {"total": programs_count},
        "events": {"total": events_count},
        "news": {"total": news_count},
        "engagement": {"subscribers": subscribers_count},
    }
