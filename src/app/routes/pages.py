"""HTML pages."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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
async def events(request: Request):
    return templates.TemplateResponse("events.html", {"request": request})


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
async def news_details(request: Request):
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
