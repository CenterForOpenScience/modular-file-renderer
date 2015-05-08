import http
import json
import asyncio

class ProviderError(Exception):
    pass
    
class DownloadError(ProviderError):
    pass
