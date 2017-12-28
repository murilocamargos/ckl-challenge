"""
This file contains the entries for article downloading though celery beat.
The periodicity of each outlet is defined by the average posting frequency,
computed by the standalone function `mtime.py`.
"""

from __future__ import absolute_import, unicode_literals

from articles.scrapers.techcrunch import TechCrunch
from articles.scrapers.cheesecakelabs import CheesecakeLabs
from articles.scrapers.mashable import Mashable
from articles.scrapers.engadget import Engadget

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from kombu.async import Hub, set_event_loop

set_event_loop(Hub())

logger = get_task_logger(__name__)



@periodic_task(
    run_every=(crontab(hour='*/5')),
    name="fetch_techcrunch_articles",
    ignore_result=True
)
def fetch_techcrunch_articles():
    logger.info("TechCrunch download just started.")
    ws = TechCrunch()
    ws.get_articles()
    logger.info("TechCrunch download finished.")



@periodic_task(
    run_every=(crontab(hour='*/14')),
    name="fetch_cheesecakelabs_articles",
    ignore_result=True
)
def fetch_cheesecakelabs_articles():
    logger.info("CheesecakeLabs download just started.")
    ws = CheesecakeLabs()
    ws.get_articles()
    logger.info("CheesecakeLabs download finished.")



@periodic_task(
    run_every=(crontab(hour='*/6')),
    name="fetch_mashable_articles",
    ignore_result=True
)
def fetch_mashable_articles():
    logger.info("Mashable download just started.")
    ws = Mashable()
    ws.get_articles()
    logger.info("Mashable download finished.")



@periodic_task(
    run_every=(crontab(hour='*/1')),
    name="fetch_engadget_articles",
    ignore_result=True
)
def fetch_engadget_articles():
    logger.info("Engadget download just started.")
    ws = Engadget()
    ws.get_articles()
    logger.info("Engadget download finished.")