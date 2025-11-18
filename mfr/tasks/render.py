import logging

from mfr.extensions.unoconv import UnoconvRenderer
from mfr.tasks import core
logger = logging.getLogger(__name__)


@core.celery_task
async def render(renderer: UnoconvRenderer):
    await renderer.do_render()
