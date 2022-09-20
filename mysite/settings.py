"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import dropbox


SECRET_KEY='django-insecure-ysels=g_*p@a)l4lffldup1*a(@mv0irf5nzkt3r4bjfjzu(1o'




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-ysels=g_*p@a)l4lffldup1*a(@mv0irf5nzkt3r4bjfjzu(1o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['social-new2.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'rest_framework_simplejwt',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'project',
    'storages',
    'login',
    
    

    
]
SITE_ID = 3

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOWED_ORIGINS = [
    'https://social-new2.herokuapp.com',
    'https://social-new2.herokuapp.com:3001',
    'https://social-new2.herokuapp.com:8000',

    'http://localhost:8000',
    'http://localhost:3001',
    "http://localhost:3000",
]
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]+ ['Set-Cookie']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



# MEDIA_ROOT =os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import datetime
from datetime import timedelta

SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
  'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
  'ROTATE_REFRESH_TOKENS': False,
  'BLACKLIST_AFTER_ROTATION': True,
  'UPDATE_LAST_LOGIN': True,

  'ALGORITHM': 'HS256',
  'SIGNING_KEY': SECRET_KEY,
  'VERIFYING_KEY': None,
  'AUDIENCE': None,
  'ISSUER': None,

  'AUTH_HEADER_TYPES': ('Bearer',),
  'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
  'USER_ID_FIELD': 'id',
  'USER_ID_CLAIM': 'user_id',
  'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
   'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
  'TOKEN_TYPE_CLAIM': 'token_type',

  'JTI_CLAIM': 'jti',

  'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
  'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
  'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

  # custom
  'AUTH_COOKIE':'access_token',  # Cookie name. Enables cookies if value is set.
  'AUTH_COOKIE_DOMAIN': None,     # A string like "example.com", or None for standard domain cookie.
  'AUTH_COOKIE_SECURE':True,    # Whether the auth cookies should be secure (https:// only).
  'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by javascript.
  'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
  'AUTH_COOKIE_SAMESITE':'Strict',  # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
}


#
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': 
        (
         'rest_framework_simplejwt.authentication.JWTAuthentication',),      
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 5
}

AUTH_USER_MODEL = 'login.CustomUser'


ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'formydjango@gmail.com'
EMAIL_HOST_PASSWORD = 'jcdwlqdjnircqilo'


# DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
# DROPBOX_OAUTH2_TOKEN='sl.BPOocd9t6Fz_URp79BfHPdcJkht5sKSvwB8MhCuzXEVEcFOjEJ05opRtj7uTafw7fygA4j-5R0XO_PX8S30HEP0K73eONldE6kEAUGxK103ftgKwZIGadun7Ab-pf_jE7397Sd4-9Ks'
# DROPBOX_APP_KEY='fodunl56jaz6wqj'
# # # DROPBOX_ROOT_PATH='/'
# DROPBOX_APP_SECRET='hxsmaesom8i7dib'
# AUTHORIZATION_CODE='-FrUu6Zx4_MAAAAAAAAAKGW0ZRolBus_xbOk997hazo'

# oauth2_refresh_token ={"access_token": "sl.BPLFqFOD1fCxoMILD0NTfP-ttZM2TXhHIOOJb-J91mq6ZK8NqT5CuQm8bHMp8bUR1HYwj9frDim0vn0NNM3XSBTNIODo8F2BpE0MqdECsCy_vc5hth9gC4CWY1WOCRUzM91z2S6DyCI",
#     "token_type": "bearer",
#     "expires_in": 14400,
#     "refresh_token": "O5eczY0ZGb4AAAAAAAAAAaiFAsEfsIuPCTbyaE-33TW7gfgkK7_COv_GKlii-pHl",
#     "scope": "account_info.read account_info.write files.content.read files.content.write files.metadata.read files.metadata.write",
#     "uid": "1387534145",
#     "account_id": "dbid:AAB4STBskDzO2qKI0V7lmlcY4DBWAUxXvZs"}
# # dbx = dropbox.Dropbox('sl.BPEZt4eQWLiAV9p5lt88_3S3PNINB2VSt9b2LSZmODh8nfmBdTVjNz5ZnWIEzsrcoRykcPAjjrjN_GcvbWkeng5uKYSgBDz9Qwq-BIXRHmPD2Cf3JOhnCtufKK_2gAqx6QO5l3ceyNM')
# # dbx.users_get_current_account()

