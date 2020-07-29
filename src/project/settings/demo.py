import os

from project.settings.base import IGN

TERRA_APPLIANCE_SETTINGS = {
    "map": {
        "accessToken": os.environ.get('MAPBOX_GL_ACCESS_TOKEN'),
        "center": [-2.9233, 47.424],
        "zoom": 10,
        "maxBounds": [[-180, -90], [180, 90]],
        "backgroundStyle": [
            {"label": "Plan", "url": "mapbox://styles/mapbox/streets-v9"},
            {"label": "Orthophoto IGN", "url": IGN},
        ],
    },
    'enabled_modules': ['OPP'],
}
