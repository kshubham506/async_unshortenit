import re
from urllib.parse import urlsplit
import aiohttp
from async_unshortenit.exceptions import AsyncNotFound
from typing import Tuple


class AsyncUnshortenModule:

    name = None
    domains = set()
    _domain_regex = None

    def __init__(self, headers: dict = None, timeout: int = 30):
        self.headers = headers
        self.timeout = timeout
        self._build_domain_regex()

    def unshorten(self, uri: str, timeout: int = None) -> str:
        raise NotImplementedError

    def _build_domain_regex(self):
        regex_str = r"^(" + r"|".join(self.domains) + r")$"
        regex_str = re.sub(r"\.", "\.", regex_str)
        self._domain_regex = re.compile(regex_str)

    async def get(
        self, uri: str, headers: dict = None, timeout: int = None
    ) -> Tuple[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=uri,
                headers=headers or self.headers,
                timeout=timeout or self.timeout,
                allow_redirects=True,
            ) as response:
                if response.status != 200:
                    raise AsyncNotFound(response.status)
                return await response.text(), str(response.url)

    def is_match(self, url):
        domain = urlsplit(url).netloc
        return self._domain_regex.match(domain)

    def add_domain(self, domain):
        self.domains.add(domain)
        self._build_domain_regex()
