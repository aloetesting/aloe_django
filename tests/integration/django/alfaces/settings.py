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
SECRET_KEY = 'secret'
STATIC_URL = '/static/'
MIDDLEWARE_CLASSES = ()
