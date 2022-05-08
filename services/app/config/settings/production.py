from .base import *  # noqa: F401, F403

# For 2.0, only have pawnguild here here
ALLOWED_HOSTS = ["pawntest.xyz", "www.pawntest.xyz"]
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True


EMAIL_USE_TLS = True
# When releasing 2.0, we will go back to ALLOWED_HOSTS[0]
# EMAIL_PAGE_DOMAIN = ALLOWED_HOSTS[0] + "/"
EMAIL_PAGE_DOMAIN = "pawntest.xyz" + "/"
