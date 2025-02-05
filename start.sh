#!/bin/bash
# Start Gunicorn and Nginx
gunicorn -c gunicorn_config.py wsgi:app &
nginx -g "daemon off;"
