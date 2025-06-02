DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "6VSq9kES6sijvuvVo57IYvOGAViNKSyM6jEwD8uVOnS0KXuRJUZ8SVWJeae66Ki3gHSbotsABHEg6b3i6z4uQPDTERuuYxSTqTDDtfpyMJPclqtLWPMeiUoQJ9EAQBm3"

ALLOWED_HOSTS = ['localhost']

STATIC_ROOT = "static_deploy/static"

RAVEN_CONFIG = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'backoffice'
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 25

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': True,
        }
    }
}
