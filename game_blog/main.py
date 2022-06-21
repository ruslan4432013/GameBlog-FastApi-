from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apps.mainapp.routers import api_router


def create_app(debug=True):
    app = FastAPI(debug=debug)
    app.mount('/static', StaticFiles(directory='game_blog/static'), name='static')
    app.include_router(api_router)
    return app
