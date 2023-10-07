# get base image alpine
FROM python:3.11

# base dir is this dir
WORKDIR /usr/src/app

# copy the tailwind binaries
COPY . ./


# install django from requirements.txt file
RUN pip install -r requirements.txt

# RUN python3 manage.py collectstatic --noinput
# RUN python3 manage.py migrate

# you should have this run when making changes to template styles using tailwindcss
# RUN ./tailwindcss -i static/css/input.css -o static/css/output.css --watch

# expose port 8000
EXPOSE 8085

# # run django server
CMD ["python3", "manage.py", "runserver"]