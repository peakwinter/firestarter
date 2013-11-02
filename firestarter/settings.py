import datetime
import os

#
# Firestarter Project Settings
# Change the below settings to match what they should be for your
# project. Make sure you change SECRET_KEY, the database info, etc!
#


# The name of your project or campaign.
PROJECT_NAME = 'Firestarter Funding Campaign'

# The address of the funding site.
PROJECT_ADDR = 'http://localhost:8000'

# The slogan to be displayed on the main page.
PROJECT_SLOGAN = 'Support our awesome project.'

# Goal amount (int) that you are trying to raise.
GOAL = 50000

# Date (datetime object) when the campaign will end
DATE = datetime.datetime.now() + datetime.timedelta(days=10)

# Disable new contributions when time runs out?
STOP = False

# The email address that notifications will come from.
# e.g. noreply@example.com
NOTIFY_SENDER = 'noreply@example.com'

# List of payment types that you will accept.
# Possible values (copy these entirely):
#   ('CC', 'Credit Card (VISA/MasterCard/AMEX)', 'icon-credit-card')
#   ('BC', 'Bitcoin', 'icon-btc')
#   ('PP', 'PayPal Account', 'icon-dollar')
PAY_TYPES = (
    ('CC', 'Credit Card (VISA/MasterCard/AMEX)', 'icon-credit-card'),
    ('BC', 'Bitcoin', 'icon-btc'),
    ('PP', 'PayPal Account', 'icon-dollar')
)

SUCCESS_DISCLAIMER = ('If you claimed a reward in connection with your contribution, '
    'shipping will begin by next month. Stay tuned to one of our social '
    'media accounts to get updates as to what rewards are shipping when.')


# Stripe API publishable key (if using Stripe for CC payments)
STRIPE_PUBLIC_KEY = ''

# Stripe API private key (if using Stripe for CC payments)
STRIPE_PRIVATE_KEY = ''

# PayPal REST API mode: 'sandbox' for testing or 'live' for real charges
PAYPAL_MODE = 'sandbox'
# PayPal REST API ID and secret.
PAYPAL_CLIENT_ID = ''
PAYPAL_CLIENT_SECRET = ''

# The Bitcoin address for people to donate to (if Bitcoin is accepted)
BTC_ADDR = ''

# API key for pulling currency exchange rates.
# Get one here: https://currency-api.appspot.com/
CURRENCY_API_KEY = ''

# Optional disclaimer to show above the list of rewards.
REWARDS_DISCLAIMER = 'All contributions of $2 or more get the donor\'s name (or appropriate pseudonym) on a special Donors page of the website.'


#####################################################################

# Django settings for firestarter project.

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Test Admin', 'test@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'firestarter',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'firestarter',
        'PASSWORD': 'firestarter',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'CHANGE_ME'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'firestarter.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'firestarter.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'firestarter/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',
    'firestarter',
    'widget_tweaks',
    'south',
    'captcha',
    'django_gravatar'
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
