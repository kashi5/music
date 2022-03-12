release: python3 manage.py migrate
web: gunicorn music.wsgi --timeout 60 --log-file