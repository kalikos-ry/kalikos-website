#!/bin/bash
set -e
gunicorn kalikos.wsgi --log-file -