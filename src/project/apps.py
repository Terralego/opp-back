from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectConfig(AppConfig):
    name = "project"

    def ready(self):
        from . import receivers  # NOQA


# Add translation here to avoid missing translation
# in terra_account module.
# FIXME
# Translation from terra-opp...
extra_translations = [
    _("Can manage viewpoints"),
    _("Can manage pictures"),
    _("Can add pictures"),
    _("Can manage campaign"),
]