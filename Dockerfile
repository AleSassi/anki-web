FROM python:3.9.18-slim-bullseye

RUN echo "Building docker image"
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

RUN echo 'alias ll="ls -al"' >> ~/.bashrc

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

ADD . /app

RUN python ./backend/manage.py makemigrations
RUN python ./backend/manage.py migrate

CMD ["python", "./backend/manage.py", "runserver", "0.0.0.0:8000"]