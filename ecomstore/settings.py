"""
Django settings for ecomstore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ommw3ci5aykure*^!$7%q1^lnxk(vv0ww_g*pjbf0(y-)fov*i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'material',
    # 'material.admin',
    # 'wpadmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'preview',
    'catalog',
    'utils_',
    'cart',
    'accounts',
    'checkout',
    'search',
    'stats',
    'tagging',
    'manager',
    'caching',
    'cookielaw',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ecomstore.SSLMiddleware.SSLRedirect',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    # 'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'ecomstore.context_processors.ecomstore',
    'django.core.context_processors.request',
    # 'django.template.context_processors.request',
)

ROOT_URLCONF = 'ecomstore.urls'

WSGI_APPLICATION = 'ecomstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True


# USE_TZ=True makes the dates and times timezone aware. This is usually required if users from different timezones need to use your app.
# si lo ponemos sale esta exc: ImproperlyConfigured: This query requires pytz, but it isn't installed.
# After continuing to search for django and pytz, I found the 1.6 Django release notes, which mention that you must now install pytz to work with Sqlite3 if USE_TZ=True in your settings.py.
# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

DATE_FORMAT = "d/M/Y"

SITE_NAME = 'Leoshop'
META_KEYWORDS = 'Music, instruments, music accessories, musician supplies'
META_DESCRIPTION = 'Modern Musician is an online supplier of instruments, sheet music, ' \
                   'and other accessories for musicians'
ENABLE_SSL = False
LOGIN_REDIRECT_URL = '/accounts/my_account/'
LOGOUT_REDIRECT_URL = ''
AUTH_PROFILE_MODULE = 'accounts.userprofile'

PRODUCTS_PER_PAGE = 6
PRODUCTS_PER_ROW = 3

# mail
EMAIL_HOST = 'smtp.estudiantes.uci.cu'
EMAIL_PORT = '25'
# are used to authenticate to the SMTP server
EMAIL_HOST_USER = 'aoviedo@estudiantes.uci.cu'
EMAIL_HOST_PASSWORD = 'test..15'
# control whether a secure connection is use
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = ''
SESSION_AGE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_AGE_DAYS
CACHE_TIMEOUT = 60 * 60 * 12

ADMIN_MEDIA_PREFIX = 'static/admin'
