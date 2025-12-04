"""
FastAPI Backend for United Youth Developers (UYD)
Provides REST API for programs, events, and other content management
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./uyd.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(
        String, index=True
    )  # education, agribusiness, leadership, environment, tourism, lifeskills
    content = Column(Text)
    featured_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    event_type = Column(
        String, index=True
    )  # workshop, seminar, competition, conference, etc.
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    location = Column(String)
    max_participants = Column(Integer, nullable=True)
    featured_image = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    registration_deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    excerpt = Column(String(500), nullable=True)
    category = Column(String, index=True)
    author = Column(String)
    publish_date = Column(DateTime, default=datetime.utcnow)
    featured_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


# Pydantic Models
class ProgramBase(BaseModel):
    title: str
    description: str
    category: str
    content: str
    featured_image: Optional[str] = None
    is_featured: bool = False
    is_active: bool = True


class ProgramCreate(ProgramBase):
    pass


class ProgramResponse(ProgramBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    title: str
    description: str
    event_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    location: str
    max_participants: Optional[int] = None
    featured_image: Optional[str] = None
    content: Optional[str] = None
    registration_deadline: Optional[datetime] = None
    is_featured: bool = False
    is_active: bool = True


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewsArticleBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    category: str
    author: str
    publish_date: datetime
    featured_image: Optional[str] = None
    is_featured: bool = False
    is_active: bool = True


class NewsArticleCreate(NewsArticleBase):
    pass


class NewsArticleResponse(NewsArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Create database tables
Base.metadata.create_all(bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI app
app = FastAPI(
    title="United Youth Developers API",
    description="Backend API for UYD website content management",
    version="1.0.0",
)

# Mount static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Template setup
templates = Jinja2Templates(directory="templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Programs API endpoints
@app.get("/api/programs/", response_model=List[ProgramResponse])
async def get_programs(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Program).filter(Program.is_active == True)

    if category:
        query = query.filter(Program.category == category)
    if featured is not None:
        query = query.filter(Program.is_featured == featured)

    programs = query.offset(skip).limit(limit).all()
    return programs


@app.get("/api/programs/featured/", response_model=List[ProgramResponse])
async def get_featured_programs(db: Session = Depends(get_db)):
    programs = (
        db.query(Program)
        .filter(Program.is_active == True, Program.is_featured == True)
        .all()
    )
    return programs


@app.get("/api/programs/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: int, db: Session = Depends(get_db)):
    program = (
        db.query(Program)
        .filter(Program.id == program_id, Program.is_active == True)
        .first()
    )
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@app.post("/api/programs/", response_model=ProgramResponse)
async def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    db_program = Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


@app.put("/api/programs/{program_id}", response_model=ProgramResponse)
async def update_program(
    program_id: int, program: ProgramCreate, db: Session = Depends(get_db)
):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    for key, value in program.dict().items():
        setattr(db_program, key, value)

    db.commit()
    db.refresh(db_program)
    return db_program


@app.delete("/api/programs/{program_id}")
async def delete_program(program_id: int, db: Session = Depends(get_db)):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    db_program.is_active = False
    db.commit()
    return {"message": "Program deleted successfully"}


# Events API endpoints
@app.get("/api/events/", response_model=List[EventResponse])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = None,
    featured: Optional[bool] = None,
    upcoming: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Event).filter(Event.is_active == True)

    if event_type:
        query = query.filter(Event.event_type == event_type)
    if featured is not None:
        query = query.filter(Event.is_featured == featured)
    if upcoming:
        query = query.filter(Event.start_date >= datetime.utcnow())

    events = query.order_by(Event.start_date).offset(skip).limit(limit).all()
    return events


@app.get("/api/events/upcoming/", response_model=List[EventResponse])
async def get_upcoming_events(db: Session = Depends(get_db)):
    events = (
        db.query(Event)
        .filter(Event.is_active == True, Event.start_date >= datetime.utcnow())
        .order_by(Event.start_date)
        .limit(10)
        .all()
    )
    return events


@app.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = (
        db.query(Event).filter(Event.id == event_id, Event.is_active == True).first()
    )
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/events/", response_model=EventResponse)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.put("/api/events/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int, event: EventCreate, db: Session = Depends(get_db)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event.dict().items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return db_event


@app.delete("/api/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db_event.is_active = False
    db.commit()
    return {"message": "Event deleted successfully"}


# News API endpoints
@app.get("/api/news/", response_model=List[NewsArticleResponse])
async def get_news(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(NewsArticle).filter(NewsArticle.is_active == True)

    if category:
        query = query.filter(NewsArticle.category == category)
    if featured is not None:
        query = query.filter(NewsArticle.is_featured == featured)

    news = (
        query.order_by(NewsArticle.publish_date.desc()).offset(skip).limit(limit).all()
    )
    return news


@app.get("/api/news/latest/", response_model=List[NewsArticleResponse])
async def get_latest_news(db: Session = Depends(get_db)):
    news = (
        db.query(NewsArticle)
        .filter(NewsArticle.is_active == True)
        .order_by(NewsArticle.publish_date.desc())
        .limit(10)
        .all()
    )
    return news


@app.get("/api/news/featured/", response_model=List[NewsArticleResponse])
async def get_featured_news(db: Session = Depends(get_db)):
    news = (
        db.query(NewsArticle)
        .filter(NewsArticle.is_active == True, NewsArticle.is_featured == True)
        .order_by(NewsArticle.publish_date.desc())
        .limit(5)
        .all()
    )
    return news


@app.get("/api/news/{article_id}", response_model=NewsArticleResponse)
async def get_news_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(NewsArticle)
        .filter(NewsArticle.id == article_id, NewsArticle.is_active == True)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/api/news/", response_model=NewsArticleResponse)
async def create_news_article(
    article: NewsArticleCreate, db: Session = Depends(get_db)
):
    db_article = NewsArticle(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


# Site stats endpoint
@app.get("/api/core/stats/")
async def get_site_stats(db: Session = Depends(get_db)):
    programs_count = db.query(Program).filter(Program.is_active == True).count()
    events_count = db.query(Event).filter(Event.is_active == True).count()
    news_count = db.query(NewsArticle).filter(NewsArticle.is_active == True).count()

    # Mock subscriber count - in real app, you'd have a subscribers table
    subscribers_count = 1250

    return {
        "programs": {"total": programs_count},
        "events": {"total": events_count},
        "news": {"total": news_count},
        "engagement": {"subscribers": subscribers_count},
    }


# Template Routes - Serve HTML pages
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
@app.get("/about.html")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/programs")
@app.get("/programs.html")
async def programs(request: Request):
    return templates.TemplateResponse("programs.html", {"request": request})


@app.get("/events")
@app.get("/events.html")
async def events(request: Request):
    return templates.TemplateResponse("events.html", {"request": request})


@app.get("/contact")
@app.get("/contact.html")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/get-involved")
@app.get("/get-involved.html")
async def get_involved(request: Request):
    return templates.TemplateResponse("get-involved.html", {"request": request})


@app.get("/news")
@app.get("/news.html")
async def news(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})


@app.get("/event-details")
@app.get("/event-details.html")
async def event_details(request: Request):
    return templates.TemplateResponse("event-details.html", {"request": request})


@app.get("/news-details")
@app.get("/news-details.html")
async def news_details(request: Request):
    return templates.TemplateResponse("news-details.html", {"request": request})


@app.get("/students-life")
@app.get("/students-life.html")
async def students_life(request: Request):
    return templates.TemplateResponse("students-life.html", {"request": request})


@app.get("/privacy")
@app.get("/privacy.html")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@app.get("/terms-of-service")
@app.get("/terms-of-service.html")
async def terms_of_service(request: Request):
    return templates.TemplateResponse("terms-of-service.html", {"request": request})


@app.get("/404")
@app.get("/404.html")
async def not_found(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
