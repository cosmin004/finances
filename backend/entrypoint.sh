#!/bin/bash
mongod --fork --logpath /var/log/mongod.log

gunicorn --bind 0.0.0.0:8080 --workers=1 --threads=10 --worker-class=gthread --timeout=0 wsgi