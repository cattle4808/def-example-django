FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD python manage.py migrate \
    && python create_super_user.py \
    && python manage.py collectstatic --noinput \
    && exec gunicorn -c gunicorn.conf.py rest.wsgi:application


