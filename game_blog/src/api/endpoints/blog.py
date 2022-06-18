from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from game_blog.core.config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
