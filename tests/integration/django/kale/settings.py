DEBUG = True

ROOT_URLCONF = 'urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
INSTALLED_APPS = (
    'lettuce_django',
    'leaves',
)

LETTUCE_TEST_SERVER = 'lettuce_django.server.DjangoServer'
SECRET_KEY = 'secret'

STATIC_URL = '/static/'
