import os
from .base import *
from dotenv import load_dotenv

load_dotenv()

if os.getenv('DJANGO_SETTINGS_MODULE') == 'app.settings.dev':
    from .dev import *
else:
    from .deploy import *

__all__ = dir()