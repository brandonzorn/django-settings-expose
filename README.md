# django-settings-expose

A modern, high-performance, and cached Django context processor that safely exposes specific settings to your templates.

This is a heavily optimized drop-in replacement for the unmaintained `django-settings-export` package.
Unlike the original implementation, `django-settings-expose` caches your exposed settings in memory at server startup,
introducing **zero performance overhead** on later template renders.

## Features

- ⚡ **Zero-overhead:** Settings are read and cached once when the server boots.
- 🔒 **Secure:** Only whitelisted settings in `SETTINGS_EXPOSE` are exposed.
- 🛑 **Fail-fast:** Throws clear, descriptive errors during development if you typo a setting name or try to access an
  unexposed variable in a template.

---

## Installation

Install the package directly from PyPI:

```bash
pip install django-settings-expose
```

---

## Configuration

1. Add the context processor to your `settings.py` inside the `TEMPLATES` configuration:

```python
# settings.py

TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            "context_processors": [
                # ...
                # Add this line:
                "django_settings_expose.settings_expose",
            ],
        },
    },
]
```

2. Define the list of settings you want to expose to your templates using `SETTINGS_EXPOSE`:

```python
# settings.py

API_VERSION = "v1.2.6"
COMPANY_NAME = "My Awesome Company"
SECRET_KEY = "super-secret"  # Keep this safe!

# Whitelist variables to be accessible in templates
SETTINGS_EXPOSE = [
    "API_VERSION",
    "COMPANY_NAME",
]
```

---

## Usage in Templates

All exposed settings are made available via a globally accessible `{{ settings }}` dictionary variable:

```html

<footer>
  <p>Copyright © 2026 {{ settings.COMPANY_NAME }}</p>
  <p>API Version: {{ settings.API_VERSION }}</p>
</footer>
```

### Error Handling

To protect you from typos and silent bugs, the library will raise explicit exceptions:

* If a variable listed in `SETTINGS_EXPOSE` is missing from `settings.py`, it throws an `UndefinedSettingError` on
  startup.
* If a template attempts to access a variable that wasn't whitelisted (e.g., `{{ settings.SECRET_KEY }}`), it
  throws an `UnexposedSettingError`.

---

## License & Acknowledgements

This project is licensed under the **BSD 3-Clause License**.

It is based on the original concept of `django-settings-export` by `Jakub Roztocil <jakub@subtleapps.com>` (Copyright ©
2014).
Modified and optimized by `Vladimir Klimenko <v.klimenko.2137@gmail.com>` (Copyright © 2026).