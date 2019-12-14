FROM python:3.8

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=./config/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

RUN python manage.py migrate --noinput

CMD python manage.py runserver 0.0.0.0:8000