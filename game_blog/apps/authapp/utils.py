import hashlib
import random
import string
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from apps.authapp import User
from apps.authapp.models import Token

from apps.authapp.schemas import UserCreate


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()

    enc = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split('$')
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str, db: Session):
    """ Возвращает информацию о пользователе """
    user = db.query(User).filter(User.email == email).first()
    return user


async def get_user_by_token(token: str, db: Session):
    user = db.query(User).join(Token).filter(and_(Token.token == token, Token.expires > datetime.now())).first()
    return user


async def get_token_by_user(user_uid: str, db: Session):
    token = db.query(Token).filter(and_(Token.user_uid == user_uid, Token.expires > datetime.now())).first()
    return token


async def create_user_token(user_uid: str, db: Session):
    token = Token(
        expires=datetime.now() + timedelta(weeks=2),
        user_uid=user_uid,
    )
    db.add(token)
    db.commit()
    return token


async def create_user(user: UserCreate, db: Session):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    user_db = User(
        username=user.username,
        email=user.email,
        hashed_password=f"{salt}${hashed_password}",
        is_active=True
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    user_uid = user_db.uid

    return {**user.dict(), 'uid': user_uid, 'is_active': True}


async def get_current_user(db: Session, token: str):
    user = await get_user_by_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user
