import sys
import os
import django

from articles.models import Outlet, Article

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cklabs.settings")

django.setup()


"""
This is a standalone django script to compute the mean frequency of posting of
each outlet. This way we can infer the periodicity of celery tasks for each one
of them.
"""

ALL_DELTAS = []

for outlet in Outlet.objects.all():

    articles = Article.objects.filter(outlet_id=outlet.id)\
        .values('date')\
        .order_by('date')


    deltas = []
    for i in range(1, len(articles)):
        delta = articles[i]['date'] - articles[i - 1]['date']
        deltas += [delta.seconds]


    ALL_DELTAS += deltas


    HOURS = (sum(deltas)/len(deltas))/60/60
    print(outlet.name + ': ' + str(HOURS))

HOURS = (sum(ALL_DELTAS)/len(ALL_DELTAS))/60/60
print('Total: ' + str(HOURS))
