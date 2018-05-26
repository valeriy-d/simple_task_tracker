FROM library/postgres
ENV POSTGRES_USER task_tracker
ENV POSTGRES_PASSWORD qwerty
ENV POSTGRES_DB task_tracker

FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
#RUN python manage.py test
CMD python manage.py runserver 0.0.0.0:8000

