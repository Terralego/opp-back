import logging
import os

import six

from .base import *  # noqa

os.environ['RELATIVE_SETTINGS_MODULE'] = '.dev'
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}
DEBUG = True
SWAGGER_ENABLED = DEBUG

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

MEDIA_URL = '/media/'

# Force every loggers to use console handler only. Note that using 'root'
# logger is not enough if children don't propage.
for logger in six.itervalues(LOGGING['loggers']):  # noqa
    logger['handlers'] = ['console']
# Log every level.
LOGGING['handlers']['console']['level'] = logging.NOTSET  # noqa

try:
    from .local import *  # noqa
except ImportError:
    pass
