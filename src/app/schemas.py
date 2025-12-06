from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel, Field


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


class ProgramCreateWithImage(ProgramCreate):
    """Program creation schema with image upload support."""

    featured_image_file: UploadFile | None = None


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


class EventCreateWithImage(EventCreate):
    """Event creation schema with image upload support."""

    featured_image_file: UploadFile | None = None


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


class EventRegistrationSchema(BaseModel):
    """Event registration Schema."""

    event_id: int = Field(gt=0)
    user_name: str = Field(
        min_length=3,
        max_length=100,
    )
    user_email: str = Field(
        pattern=r"^[^@]+@[^@]+\.[^@]+$",
        description="Valid email address",
    )
    user_mobile_number: str = Field(
        min_length=10,
        max_length=15,
    )
