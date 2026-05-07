from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 SECURITY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key')

# 🔥 AUTO DEBUG (local=True, render=False)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = ['*']  # deploy ke baad domain daalna


# 📦 INSTALLED APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'myapp',
    'rest_framework',
    'django.contrib.sites',
]

SITE_ID = 1

# ⚙️ MIDDLEWARE (correct order)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 🔥 static ke liye
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 🔐 important
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 🔗 URL CONFIG
ROOT_URLCONF = 'myproject.urls'


# 🧾 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ⚡ WSGI
WSGI_APPLICATION = 'myproject.wsgi.application'


# 🗄 DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 🔐 PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 🌍 LANGUAGE & TIME
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# 🎨 STATIC FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "myproductionstaticfiles"

# 🔥 Production static handling
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# 📧 EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("ankitparmar8126@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("bessabqlcvzyrjvu")