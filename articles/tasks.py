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
    run_every=(crontab(minute=0,hour='0,6,8,10,12,14,16,18,20,22')),
    name="fetch_articles",
    ignore_result=True
)
def fetch_articles():
    ws = TechCrunch()
    if ws.outlet.active:
        logger.info("TechCrunch download just started.")
        ws.get_articles()
        logger.info("TechCrunch download finished.")

    ws = CheesecakeLabs()
    if ws.outlet.active:
        logger.info("CheesecaekLabs download just started.")
        ws.get_articles()
        logger.info("CheesecakeLabs download finished.")

    ws = Mashable()
    if ws.outlet.active:
        logger.info("Mashable download just started.")
        ws.get_articles()
        logger.info("Mashable download finished.")

    ws = Engadget()
    if ws.outlet.active:
        logger.info("Engadget download just started.")
        ws.get_articles()
        logger.info("Engadget download finished.")