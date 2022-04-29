"""
Django settings for pawnhall project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from django.core.exceptions import ImproperlyConfigured

import os
from pathlib import Path

# flake8: noqa


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "pawnguild"

SECRET_KEY = get_env_variable("SECRET_KEY")

# Application definition

INSTALLED_APPS = [
    "pawnguild.pawnguild_common",
    "pawnguild.pawnlisting",
    "pawnguild.registration",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_nose",
    "django_email_verification",
    "password_reset",
    "django_cleanup",
    "django_unused_media",
]

MIDDLEWARE = [
    "pawnguild.pawnguild_common.middleware.LogErrors.LogErrorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "pawnguild.pawnlisting.backends.EmailAuthBackend",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "registration.UserProfile"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Settings for django_email_verification and reset_password

DEFAULT_FROM_EMAIL = "PawnGuild <pawnhall7@gmail.com>"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "pawnhall7@gmail.com"
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_TOKEN_LIFE = 60 * 60  # email is valid for 1 hour


def verified_callback(user):
    user.email_verified = True


EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "PawnGuild <pawnhall7@gmail.com>"
EMAIL_FROM_ADDRESS = "PawnGuild <pawnhall7@gmail.com>"
EMAIL_PASSWORD = get_env_variable("EMAIL_PASSWORD")
EMAIL_MAIL_SUBJECT = "Activate your PawnGuild Account"
EMAIL_MAIL_HTML = "confirmation_email.html"
EMAIL_MAIL_PLAIN = "confirmation_email.txt"
EMAIL_PAGE_TEMPLATE = "email_page.html"

# End django_email_verificaiton settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
