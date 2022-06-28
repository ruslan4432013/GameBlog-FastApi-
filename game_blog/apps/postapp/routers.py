import os

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from fastapi.requests import Request

from apps.postapp import Post
from apps.postapp.forms import AddPostForm
from core.config import TemplateResponse, MEDIA_URL
from core.decorators import login_required
from core.requests_framework import setup_user_dict
from db.session import get_db

post_route = APIRouter(prefix='/blog')


@post_route.get('/')
async def all_post(request: Request, db: Session = Depends(get_db)):
    request.name = 'blog'
    response_dict = await setup_user_dict(request, db)
    posts = db.query(Post).order_by(Post.created_date.desc()).all()

    response_dict['posts'] = posts

    return TemplateResponse('blog/blog.jinja2', response_dict)


@post_route.get('/add_post/')
@post_route.post('/add_post/')
@login_required
async def create_post(request: Request, db: Session = Depends(get_db)):
    request.name = 'add_post'
    response_dict = await setup_user_dict(request, db)

    if request.method == "POST":
        form = AddPostForm(request, context=response_dict)

        is_created = await form.create_post(db)
        if is_created:
            response_dict.update({'success': True})
        else:
            response_dict.update(form.__dict__)

    return TemplateResponse('blog/create_post.jinja2', response_dict)
