import datetime
import json

from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import status
from apps.authapp.form import UserCreateForm, UserLoginForm, UserUpdateForm
from apps.authapp.schemas import UserCreate, TokenBase
from core.config import TemplateResponse
from secrets import token_urlsafe
from db.repository.users import create_new_user
from db.session import get_db
from fastapi import responses
from sqlalchemy.exc import IntegrityError
from .models import User, Token
from uuid import UUID

from .utils import get_user_by_email, create_user, validate_password, get_user_by_token, get_token_by_user, \
    create_user_token

user_router = APIRouter()


@user_router.post('/register/')
@user_router.get('/register/')
async def register(request: Request, db: Session = Depends(get_db)):
    if request.method == 'GET':
        return TemplateResponse("auth/register.html", {"request": request})
    else:
        form = await request.form()
        form_register_data = {
            'username': form.get('username'),
            'email': form.get('email'),
            'password': form.get('password'),
        }
        user = UserCreate(**form_register_data)
        db_user = await get_user_by_email(email=user.email, db=db)
        if db_user:
            return TemplateResponse("auth/register.html", {"request": request,
                                                           "error": 'User with this email has already'})
        else:
            new_user = await create_user(user, db)
            return TemplateResponse("auth/login.html", {"request": request})


@user_router.post('/update/')
@user_router.get('/update/')
async def update(request: Request, db: Session = Depends(get_db)):
    if request.method == 'GET':
        return TemplateResponse("auth/update.html", {"request": request})
    else:
        form = UserUpdateForm(request)
        await form.load_data()
        if await form.is_valid(db):
            try:
                user = db.query(User).filter(User.username == form.old_name).first()
                if form.username:
                    user.username = form.username
                if form.email:
                    user.email = form.email
                db.commit()
                return responses.JSONResponse({'status': 'success', 'user': user.username})
            except IntegrityError:
                form.__dict__.get("errors").append("Duplicate username or email")
                return TemplateResponse("auth/update.html", form.__dict__)

        return TemplateResponse("auth/update.html", form.__dict__)


@user_router.post('/login/')
@user_router.get('/login/')
async def login_page(request: Request, db: Session = Depends(get_db)):
    if request.method == "GET":
        return TemplateResponse('auth/login.html', {'request': request})

    form = await request.form()

    user = await get_user_by_email(form.get('email'), db)

    if not user:
        return TemplateResponse('auth/login.html', {'request': request, 'error': 'Incorrect email or password'})

    if not validate_password(password=form.get('password'), hashed_password=user.hashed_password):
        return TemplateResponse('auth/login.html', {'request': request, 'error': 'Incorrect email or password'})

    response = responses.RedirectResponse('/?msg=Successfully-Logged')

    token = await create_user_token(user.uid, db)
    response.set_cookie('token', token.token)
    return response


@user_router.get('/logout/')
async def logout(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('token')
    token_db = db.query(Token).filter(Token.token == token).first()
    db.delete(token_db)
    db.commit()
    response = responses.RedirectResponse('/')
    response.delete_cookie('token')
    return response
