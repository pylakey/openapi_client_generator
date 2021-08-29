import httpx

from .models import *


class Client(httpx.AsyncClient):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
