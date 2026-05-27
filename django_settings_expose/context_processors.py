"""
Modern implementation of Django settings exporter to templates.
Based on django-settings-export by Jakub Roztocil.

Original work Copyright © 2014 Jakub Roztocil <jakub@subtleapps.com>
Modified work Copyright © 2026 Vladimir Klimenko <v.klimenko.2137@gmail.com>

Licensed under the MIT License.
The original component is licensed under the BSD 3-Clause License.
See the LICENSE file in the root of this project for full license texts.
"""

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


class SettingsExposeError(ImproperlyConfigured):
    """Base error indicating misconfiguration."""


class UndefinedSettingError(SettingsExposeError):
    """An undefined setting name included in SETTINGS_EXPOSE."""


class UnexposedSettingError(SettingsExposeError):
    """An unexposed setting has been accessed from a template."""


class ExposedSettings(dict):
    def __init__(self, settings_obj, **kwargs):
        super().__init__(**kwargs)
        for var in getattr(settings_obj, "SETTINGS_EXPOSE", []):
            try:
                self[var] = getattr(settings_obj, var)
            except AttributeError:
                raise UndefinedSettingError(
                    f"'{var}' is included in SETTINGS_EXPOSE "
                    f"but it does not exist in settings.py!",
                )

    def __missing__(self, key):
        if hasattr(self, key):
            raise KeyError(key)
        raise UnexposedSettingError(
            f"The 'settings.{key}' variable is not accessible from templates. "
            f"Please add '{key}' to the SETTINGS_EXPOSE list in settings.py.",
        )


CONTEXT_CACHE = {"settings": ExposedSettings(settings_obj=django_settings)}


def settings_expose(_):
    return CONTEXT_CACHE


__all__ = [
    "settings_expose",
    "SettingsExposeError",
    "UndefinedSettingError",
    "UnexposedSettingError",
]
