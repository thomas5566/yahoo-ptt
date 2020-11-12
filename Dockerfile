FROM python:3.7-alpine
MAINTAINER Thomnas 5566

# tells python to run in unbuffered mode
# which is recommened when running python within Docker containers
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
# copy from directory adjacemt to the Docker file
COPY requirements.txt /code/
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
# copy local mochine app folder to the Docker image app folder
COPY . /code/