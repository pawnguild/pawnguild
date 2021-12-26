from .base import *  # noqa: F401, F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# For 2.0, only have localhost here
ALLOWED_HOSTS = ["localhost", "137.184.81.130", "pawntest.xyz"]
EMAIL_PAGE_DOMAIN = "localhost:8000/"
