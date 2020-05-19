# Use the official image as a parent image.
#FROM python:3.6

#ADD . /nc_craft_breweries

# Set the working directory.
#WORKDIR /nc_craft_breweries

# Run the command inside your image filesystem.
#RUN pip install -r requirements.txt

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8080

# Copy the rest of your app's source code from your host to your image filesystem.
#COPY . .

FROM ubuntu:16.04

MAINTANER Your Name "pharmon9847@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
