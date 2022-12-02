# FROM python:3.9-slim

# WORKDIR /app

# ADD requirements.txt /app/requirements.txt

# RUN pip install --upgrade pip

# RUN pip install -r /app/requirements.txt

# ADD ./ /app/

# EXPOSE 8080

# # CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers=1", "--threads=10", "--worker-class=gthread", "--timeout=120", "wsgi"]
# # ENTRYPOINT [ "gunicorn -b 0.0.0.0:8080 --workers=1 --threads=10 --worker-class=gthread --timeout=120 wsgi" ]
# ENTRYPOINT [ "sh", "/app/entrypoint.sh"]

FROM mongo:latest

RUN apt-get update && apt-get install -y build-essential python3.9
RUN apt-get install -y python-setuptools
RUN apt-get install -y python3-pip
RUN apt-get install -y nano
RUN apt-get install -y telnet
RUN apt-get install -y vim

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

ADD ./ /app/

EXPOSE 8080

ENTRYPOINT [ "sh", "/app/entrypoint.sh"]

# FROM       ubuntu:16.04

# # Installation:
# RUN apt-get update && apt-get install -y build-essential python3.9
# RUN apt-get install -y python-setuptools
# RUN apt-get install -y python-pip
# RUN apt-get install -y nano
# RUN apt-get install -y telnet
# RUN apt-get install -y vim

# # Import MongoDB public GPG key AND create a MongoDB list file
# RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv 7F0CEB10
# RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# # Update apt-get sources AND install MongoDB
# RUN apt-get update && apt-get install -y mongodb-org

# # Create the MongoDB data directory
# RUN mkdir -p /data/db

# # Create the MongoDB data directory
# RUN mkdir -p /data/code

# # Expose port #27017 from the container to the host
# WORKDIR /app

# ADD requirements.txt /app/requirements.txt

# RUN pip install --upgrade pip

# RUN pip install -r /app/requirements.txt

# ADD ./ /app/

# EXPOSE 27017
# EXPOSE 8080
# ENTRYPOINT [ "sh", "/app/entrypoint.sh"]