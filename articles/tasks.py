# Create your tasks here
from __future__ import absolute_import, unicode_literals
from articles.models import Author, Category, Outlet, Article

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)