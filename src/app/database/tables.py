from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base

from src.app.database.config import engine

Base = declarative_base()


# Database Models
class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(
        String,
        index=True,
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
        String,
        index=True,
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


Base.metadata.create_all(bind=engine)
