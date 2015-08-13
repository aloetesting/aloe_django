DEBUG = True

ROOT_URLCONF = 'kale.urls'
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
)
SECRET_KEY = 'secret'
STATIC_URL = '/static/'
MIDDLEWARE_CLASSES = ()
