import os


def add_settings(request):
    return {
        'MAPBOX_GL_ACCESS_TOKEN': os.environ.get('MAPBOX_GL_ACCESS_TOKEN'),
    }
