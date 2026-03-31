from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-z!6#_fs*hmju%)pg7&=ae##hd*c$-9x8%nd)!x2s^5^s4nxf6h'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
