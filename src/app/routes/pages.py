"""HTML pages."""

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.app.database.config import get_db
from src.app.database.tables import Event

base_dir = Path(__file__).parent.parent.parent


router = APIRouter()


# Template setup
templates = Jinja2Templates(directory=str(base_dir / "templates"))


# Template Routes - Serve HTML pages
@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/about")
@router.get("/about.html")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/programs")
@router.get("/programs.html")
async def programs(request: Request):
    return templates.TemplateResponse("programs.html", {"request": request})


@router.get("/events")
@router.get("/events.html")
async def events(
    request: Request,
    db_session: Session = Depends(get_db),
    search: str | None = None,
    event_type: str | None = None,
):
    # Base query - events that are active and have not ended yet
    query = (
        db_session.query(Event)
        .filter(Event.is_active)
        .filter(Event.end_date >= datetime.now())
    )

    # Apply search filter (case-insensitive search in title and description)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Event.title.ilike(search_term)) | (Event.description.ilike(search_term)),
        )

    # Apply event type filter
    if event_type:
        query = query.filter(Event.event_type == event_type)

    # Get filtered events (limit to 17)
    events = query.order_by(Event.start_date).offset(0).limit(17).all()



    event_type_counts = (
        db_session.query(Event.event_type, func.count(Event.id))
        .filter(Event.is_active)
        .filter(Event.end_date >= datetime.now())
        .group_by(Event.event_type)
        .all()
    )

    # Get total count
    total_count = (
        db_session.query(func.count(Event.id))
        .filter(Event.is_active)
        .filter(Event.end_date >= datetime.now())
        .scalar()
    )

    if events:
        events = [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_date": event.start_date.strftime("%Y-%m-%d"),
                "start_time": event.start_date.strftime("%I:%M %p"),
                "start_day": event.start_date.strftime("%d"),
                "start_month": event.start_date.strftime("%b").upper(),
                "start_year": event.start_date.strftime("%Y"),
                "end_date": event.end_date.strftime("%Y-%m-%d")
                if event.end_date
                else None,
                "location": event.location,
                "event_type": event.event_type,
                "is_featured": event.is_featured,
                "max_participants": event.max_participants,
                "featured_image": event.featured_image
                or "assets/img/education/events-3.webp",
                "registration_deadline": event.registration_deadline.strftime(
                    "%Y-%m-%d",
                )
                if event.registration_deadline
                else None,
            }
            for event in events
        ]

    return templates.TemplateResponse(
        "events.html",
        {
            "request": request,
            "events": events,
            "event_type_counts": event_type_counts,
            "total_count": total_count,
            "search": search,
            "event_type": event_type,
        },
    )


@router.get("/contact")
@router.get("/contact.html")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@router.get("/get-involved")
@router.get("/get-involved.html")
async def get_involved(request: Request):
    return templates.TemplateResponse("get-involved.html", {"request": request})


@router.get("/news")
@router.get("/news.html")
async def news(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})


@router.get("/event-details")
@router.get("/event-details.html")
async def event_details(request: Request):
    return templates.TemplateResponse("event-details.html", {"request": request})


@router.get("/news-details")
@router.get("/news-details.html")
async def news_details(request: Request,id:int, db_session: Session = Depends(get_db)):
    news = db_session.query(Event).filter(Event.id == id).first()
    return templates.TemplateResponse("news-details.html", {"request": request})


@router.get("/students-life")
@router.get("/students-life.html")
async def students_life(request: Request):
    return templates.TemplateResponse("students-life.html", {"request": request})


@router.get("/privacy")
@router.get("/privacy.html")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@router.get("/terms-of-service")
@router.get("/terms-of-service.html")
async def terms_of_service(request: Request):
    return templates.TemplateResponse("terms-of-service.html", {"request": request})


@router.get("/404")
@router.get("/404.html")
async def not_found(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})
