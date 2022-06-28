from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apps.mainapp.routers import api_router


def create_app(debug=True):
    app = FastAPI(debug=debug)
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.mount('/media', StaticFiles(directory='media'), name='media')
    app.include_router(api_router)
    return app
