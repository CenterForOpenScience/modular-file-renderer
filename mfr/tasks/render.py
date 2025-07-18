import logging

from mfr.tasks import core
logger = logging.getLogger(__name__)


@core.celery_task
async def render(*args, **kwargs):
    logger.critical(f'Received task with {args=} and {kwargs=}')
