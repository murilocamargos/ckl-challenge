# Create your tasks here
from __future__ import absolute_import, unicode_literals

from articles.scrapers.techcrunch import TechCrunch
from articles.scrapers.cheesecakelabs import CheesecakeLabs
from articles.scrapers.mashable import Mashable

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from kombu.async import Hub, set_event_loop

set_event_loop(Hub())

logger = get_task_logger(__name__)



@periodic_task(
    run_every=(crontab(hour='*/3')),
    name="fetch_techcrunch_articles",
    ignore_result=True
)
def fetch_techcrunch_articles():
    logger.info("TechCrunch download just started.")
    ws = TechCrunch()
    ws.get_articles()
    logger.info("TechCrunch download finished.")



@periodic_task(
    run_every=(crontab(hour='*/12')),
    name="fetch_cheesecakelabs_articles",
    ignore_result=True
)
def fetch_cheesecakelabs_articles():
    logger.info("CheesecakeLabs download just started.")
    ws = CheesecakeLabs()
    ws.get_articles()
    logger.info("CheesecakeLabs download finished.")



@periodic_task(
    run_every=(crontab(hour='*/5')),
    name="fetch_mashable_articles",
    ignore_result=True
)
def fetch_mashable_articles():
    logger.info("Mashable download just started.")
    ws = Mashable()
    ws.get_articles()
    logger.info("Mashable download finished.")