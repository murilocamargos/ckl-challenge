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

LOGGER = get_task_logger(__name__)



@periodic_task(
    run_every=(crontab(minute=0, hour='0,6,8,10,12,14,16,18,20,22')),
    name="fetch_articles",
    ignore_result=True
)
def fetch_articles():
    """This function fetches articles from 4 different sources periodically."""
    scraper = TechCrunch()
    if scraper.outlet.active:
        LOGGER.info("TechCrunch download just started.")
        scraper.get_articles()

    scraper = CheesecakeLabs()
    if scraper.outlet.active:
        LOGGER.info("CheesecaekLabs download just started.")
        scraper.get_articles()

    scraper = Mashable()
    if scraper.outlet.active:
        LOGGER.info("Mashable download just started.")
        scraper.get_articles()

    scraper = Engadget()
    if scraper.outlet.active:
        LOGGER.info("Engadget download just started.")
        scraper.get_articles()
