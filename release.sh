#!/bin/bash
set -e

python manage.py compilescss
python manage.py collectstatic --noinput