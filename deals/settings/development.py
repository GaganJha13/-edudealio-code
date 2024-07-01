import os

# DEBUG for development
DEBUG = True

# Allowed hosts for development including local server
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

if os.getenv("POSTNAME"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("POSTNAME"),
            'USER': os.getenv("POSTUSER"),
            'PASSWORD': os.getenv("POSTPASSWORD"),
            'HOST': os.getenv("POSTHOST"),
            'PORT': os.getenv("POSTPORT"),
        }
    }
else:
    # sqlite3 database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }