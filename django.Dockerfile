# get base image alpine
FROM python:3.11-alpine

# base dir is this dir
WORKDIR /usr/src/app

# copy the tailwind binaries
COPY . ./
COPY ./*.json ./

# add psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install django from requirements.txt file
RUN pip3 install -r requirements.txt

# RUN python3 manage.py collectstatic --noinput
# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate


# install node and npm
RUN apk add --update nodejs npm

# install dependencies
RUN npm install

# expose port 8000
EXPOSE 8085
