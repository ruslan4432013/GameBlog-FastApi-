from fastapi import APIRouter
from fastapi.requests import Request
from fastapi import Depends

from sqlalchemy.orm import Session

from apps.authapp.schemas import UserCreate
from core.config import TemplateResponse
from db.session import get_db
from fastapi import responses
from .models import Token

from .utils import get_user_by_email, create_user, validate_password, create_user_token

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


@user_router.post('/login/')
@user_router.get('/login/')
async def login_page(request: Request, db: Session = Depends(get_db)):
    if request.method == "GET":
        return TemplateResponse('auth/login.html', {'request': request})

    form = await request.form()

    user = await get_user_by_email(form.get('email'), db)

    if not user or not validate_password(password=form.get('password'), hashed_password=user.hashed_password):
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
