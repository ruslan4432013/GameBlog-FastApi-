from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from apps.authapp.routers import user_router
from apps.authapp.utils import get_current_user
from core.config import TemplateResponse
from db.session import get_db

api_router = APIRouter()
api_router.include_router(user_router)


@api_router.get("/", response_class=HTMLResponse)
@api_router.post("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('token')
    response_dict = {'request': request}

    if token:
        user = await get_current_user(db, token)
        response_dict['user'] = user

    return TemplateResponse('index.html', response_dict)
