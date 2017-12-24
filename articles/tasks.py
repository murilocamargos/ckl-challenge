# Create your tasks here
from __future__ import absolute_import, unicode_literals
from articles.scrapers.techcrunch import TechCrunch

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/120')),
    name="fetch_techcrunch_articles",
    ignore_result=True
)
def fetch_techcrunch_articles():
    logger.info("TechCrunch download just started.")
    ws = TechCrunch()
    ws.get_articles()
    logger.info("TechCrunch download finished.")