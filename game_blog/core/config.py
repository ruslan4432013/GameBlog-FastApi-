import os
from fastapi.templating import Jinja2Templates

SECRET_KEY = b"SECRET_KEY"
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)


SQLALCHEMY_DATABASE_URL = 'sqlite:///./site.db'

templates = Jinja2Templates(directory="game_blog/templates")