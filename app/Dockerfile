FROM python:3.8.3-alpine
# MAINTAINER Thomnas 5566

# set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
# copy from directory adjacemt to the Docker file
COPY ./requirements.txt .

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# use apckage manager apk add a package
# --no-cache means don't store the registry index on docker file
# because docker container for application has the smallest footprint possible
RUN apk add --update --no-cache postgresql-client
RUN apk add --no-cache libffi-dev \
                       libxml2-dev \
                       libxslt-dev \
                       python3-dev \
                       gcc \
                       build-base \
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev
# --virtual sets up an alias for our dependencies that we can use to easily remove all those dependencies later
# .tmp-build-deps basically temporary build dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

# take /requirements.txt installs it using pip into the Docker image
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy local mochine app folder to the Docker image app folder
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]