#!/bin/bash

set -euxo pipefail

python manage.py migrate --no-input
gunicorn --bind :8000 --workers 2 loan_api.wsgi