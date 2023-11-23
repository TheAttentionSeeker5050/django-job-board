# get base image alpine
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE website.settings

# base dir is this dir
WORKDIR /usr/src/app

# copy the tailwind binaries
COPY . ./
COPY ./*.json ./

# add psycopg2 dependencies and remove cache
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev -- \
    && rm -rf /var/cache/apk/*  

# install django from requirements.txt file
RUN pip3 install -r requirements.txt --no-cache-dir

# RUN python3 manage.py collectstatic --noinput
# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate


# install node and npm
RUN apk add --update nodejs npm -- \
    && rm -rf /var/cache/apk/*


# install dependencies
RUN npm install

# build tailwind
RUN npm run build-tailwind

# expose port 8000
EXPOSE 5000

CMD ["gunicorn","--bind", ":5000", "website.wsgi:application"]