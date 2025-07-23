import logging

from mfr.tasks import core

logger = logging.getLogger(__name__)


@core.celery_task
async def export(exporter):
    exporter.do_export()
