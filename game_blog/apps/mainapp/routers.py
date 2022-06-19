from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from core.config import TemplateResponse

main_router = APIRouter()

@main_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return TemplateResponse('index.html', {'request': request})

