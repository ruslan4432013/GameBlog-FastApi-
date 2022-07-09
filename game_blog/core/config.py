import os
from pathlib import Path
from fastapi.templating import Jinja2Templates

from fastapi_mail import ConnectionConfig


SECRET_KEY = bytes(os.getenv('SECRET_KEY', os.urandom(32)))

SQLALCHEMY_DATABASE_URL = 'sqlite:///../site.db'

ROOT_URL = Path(__file__).resolve().parent.parent
MEDIA_URL = os.path.join(ROOT_URL, 'media')
templates = Jinja2Templates(directory="templates")


TemplateResponse = templates.TemplateResponse


mail_conf = ConnectionConfig(
    MAIL_USERNAME="NinjaEasyCool",
    MAIL_PASSWORD="amlqwmkvkekwltdg",
    MAIL_FROM="NinjaEasyCool@yandex.ru",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_FROM_NAME="no-reply",
    MAIL_TLS=False,
    MAIL_SSL=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
