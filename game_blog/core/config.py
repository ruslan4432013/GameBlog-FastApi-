import os
from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

SECRET_KEY = b"SECRET_KEY"
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)


SQLALCHEMY_DATABASE_URL = 'sqlite:///../site.db'

ROOT_URL = Path(__file__).resolve().parent.parent
MEDIA_URL = os.path.join(ROOT_URL, 'media')
templates = Jinja2Templates(directory="templates")

TemplateResponse = templates.TemplateResponse
