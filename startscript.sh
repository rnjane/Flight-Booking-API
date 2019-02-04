#!/usr/bin/env bash

set -o errexit
set -o pipefail

redis-server --daemonize yes
celery -A src/bookingapi beat -l info --detach
celery -A src/bookingapi worker -l info --detach
python3 src/manage.py runserver 0.0.0.0:8000