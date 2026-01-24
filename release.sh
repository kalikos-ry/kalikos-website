#!/bin/bash
set -e

python manage.py compilescss --use-storage
python manage.py collectstatic --noinput