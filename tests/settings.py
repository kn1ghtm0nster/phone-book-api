from config.settings import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# Fast, isolated DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Quieter logs during tests
LOGGING["root"]["level"] = "CRITICAL"
for k in LOGGING.get("loggers", {}):
    LOGGING["loggers"][k]["level"] = "CRITICAL"


# Disable logging during tests (no console, no files)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {"class": "logging.NullHandler"},
    },
    "root": {
        "handlers": ["null"],
        "level": "CRITICAL",
    },
}
