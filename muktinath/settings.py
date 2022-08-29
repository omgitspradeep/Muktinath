from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+m_$*^s*32851^-o4b!34$f6t*e-_!%ytpl-j6c@bt43$z#nq('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','muktinath.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',                                   # It is a hook for associating objects and functionality to a particular website (Here, Used for OAuth)
    'modeltranslation',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    #Our apps
    'accountapp',
    'base',
    'Marriage',
    'Birthday',


    #CELERY
    'django_celery_results',
    'django_celery_beat',


    # For OAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    #misc
    'crispy_forms',
    'import_export',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'muktinath.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',           # for OAuth

            ],
        },
    },
]

# for OAuth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


WSGI_APPLICATION = 'muktinath.wsgi.application'


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



#Invitation link's sub part used in url.py, models.py, admin.py or resources.py . This is for DRY approach.
INVITATION_SUB_PART ='/you-are-invited/'

SITE_URL = 'muktinath.herokuapp.com'

# Internationalization

#LANGUAGE_CODE = 'ne'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'
#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
SESSION_COOKIE_NAME ='guestsession'



# Assigning Custom user as default auth USER and migrate after writting this line else we'll get IntegrityError or ForeignKey Constraint while updating Customer
AUTH_USER_MODEL = 'accountapp.Customer'


#Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 

EMAIL_HOST_USER = 'rulz.dambag@gmail.com'
EMAIL_HOST_PASSWORD = 'uypykplczzorwhaf'

#We store our credentials in ".env" file and we further use "gitignore" to not send ".env" file  in hosting.
#EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_USE_TLS =  True




REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=40),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',


}

PASSWORD_RESET_TIMEOUT = 900 # 900 SEC = 15 MIN  is the time required for user to reset his account password else token expires.

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "https://muktinath.herokuapp.com"
]





# TASK SCHEDULING: CELERY

    #Configure Redis server
CELERY_BROKER_URL = 'redis://localhost:6379'   # Tells Celery how to find Redis
CELERY_ACCEPT_CONTENT = ['application/json']  
CELERY_TASK_SERIALIZER = 'json'  
CELERY_RESULT_SERIALIZER = 'json'  
CELERY_TIMEZONE = "Asia/Kathmandu"
CELERY_RESULT_BACKEND = 'django-db'   


    # CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'



#PAYMENT GATEWAY
    #Khalti
KHALTI_SECRET_KEY = ""
KHALTI_VERIFY_URL = "https://khalti.com/api/v2/payment/verify/"





# For OAuth

SITE_ID = 1
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT_URL ='account_login'

# To specify what data we need from google
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    }
}
ACCOUNT_SESSION_REMEMBER = True

# To store email address in User
SOCIALACCOUNT_QUERY_EMAIL= True
SOCIALACCOUNT_EMAIL_REQUIRED= True


CRISPY_TEMPLATE_PACK= 'bootstrap4'

