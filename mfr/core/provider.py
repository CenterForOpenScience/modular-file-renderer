import os
import asyncio

import furl
import aiohttp

class BaseProvider(metaclass=abc.ABCMeta):

    def __init__(self, credentials):
        self.credentials = credentials

    
