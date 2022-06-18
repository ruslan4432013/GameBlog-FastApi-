from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routers import api_router
from db.session import engine
from src import users, posts
from src.users import models
from src.posts import models


def create_app(debug=True):
    app = FastAPI(debug=debug)
    users.models.Base.metadata.create_all(bind=engine)
    posts.models.Base.metadata.create_all(bind=engine)
    app.mount('/static', StaticFiles(directory='game_blog/static'), name='static')
    app.include_router(api_router)
    return app
