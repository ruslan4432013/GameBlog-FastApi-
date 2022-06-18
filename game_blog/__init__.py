from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routers import api_router
from .src import users

from .db.session import engine

from game_blog.src.users import models
from .src.posts import models

src.users.models.Base.metadata.create_all(bind=engine)
src.posts.models.Base.metadata.create_all(bind=engine)

def create_app(debug=True):
    app = FastAPI(debug=debug)
    app.mount('/static', StaticFiles(directory='game_blog/static'), name='static')
    app.include_router(api_router)
    return app
