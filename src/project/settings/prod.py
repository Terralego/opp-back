from __future__ import absolute_import, division, print_function

from .base import *  # noqa

# SECURITY #

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
DEBUG = False

# Suppose we are using HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False
AWS_S3_SECURE_URLS = True

# We need the staticfiles to be collected at least for PDF generation
# STATICFILES_DIRS = []
MEDIA_ACCEL_REDIRECT = False

try:
    from .local import *  # noqa
except ImportError:
    pass
