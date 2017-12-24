web: gunicorn cklabs.wsgi --log-file -
worker: celery -A cklabs worker -events -loglevel info 
beat: celery -A cklabs beat