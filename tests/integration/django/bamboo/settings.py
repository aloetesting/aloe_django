#

DEBUG = True

ROOT_URLCONF = 'urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'garden-db.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
INSTALLED_APPS = (
    'aloe_django',
    'leaves',
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
