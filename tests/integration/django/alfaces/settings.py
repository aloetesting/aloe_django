#

DEBUG = True

ROOT_URLCONF = 'alfaces.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'aloe_django',
    'donothing',
    'foobar',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

SECRET_KEY = 'secret'
STATIC_URL = '/static/'
MIDDLEWARE_CLASSES = ()
