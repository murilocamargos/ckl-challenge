web: newrelic-admin run-program gunicorn cklabs.wsgi --log-file -
worker: celery -A cklabs worker -B --loglevel=INFO