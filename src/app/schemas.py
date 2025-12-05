from datetime import datetime

from pydantic import BaseModel


# Pydantic Models
class ProgramBase(BaseModel):
    title: str
    description: str
    category: str
    content: str
    featured_image: str | None = None
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
    end_date: datetime | None = None
    location: str
    max_participants: int | None = None
    featured_image: str | None = None
    content: str | None = None
    registration_deadline: datetime | None = None
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
    excerpt: str | None = None
    category: str
    author: str
    publish_date: datetime
    featured_image: str | None = None
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
