DEBUG = True

ALLOWED_HOSTS = ['*']  # allow all

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'music',
            'HOST': 'localhost',
            'PORT': '5432',
            'USER': 'postgres',
            'PASSWORD': ''
        }
}