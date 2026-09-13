"""Synthetic local/CI tests with no connection to production PostgreSQL."""
import os
import tempfile

for key in (
    "SECRET_KEY",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "EMAIL_PASSWORD",
):
    os.environ.setdefault(key, "unused-local-test-value")

from .test import *  # noqa: F401,F403,E402

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"null": {"class": "logging.NullHandler"}},
    "root": {"handlers": ["null"]},
}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
MEDIA_ROOT = tempfile.mkdtemp(prefix="pawnguild-test-media-")
