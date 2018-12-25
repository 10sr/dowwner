# -*- mode: python -*-

import os

LOGIN_URL = "/dowwner/login/"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.environ["DOWWNER_BASE_DIR"]

ROOT_URLCONF = "dowwner.urls"

WSGI_APPLICATION = "dowwner.wsgi.application"

INSTALLED_APPS = [
    "dowwner.app.apps.DowwnerConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "ja-jp"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = "/dowwner/static/"
