from typing import List
import aiohttp
from module import AsyncUnshortenModule
from modules import AdfLy, AdFocus, ShorteSt, MetaRefresh
from __version__ import __version__


DEFAULT_HEADERS = {
    "User-Agent": "unshortenit {}".format(__version__),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
}


class AsyncUnshortenIt:

    modules = {}
    _default_headers = None
    _default_timeout = None

    def __init__(self, default_timeout: int = 30, default_headers: dict = None):
        self._default_headers = default_headers or DEFAULT_HEADERS
        self._default_timeout = default_timeout

        self.register_modules([AdfLy, AdFocus, ShorteSt, MetaRefresh])

    def register_module(self, module: AsyncUnshortenModule):
        if not isinstance(module, AsyncUnshortenModule):
            module = module(
                headers=self._default_headers, timeout=self._default_timeout
            )
        self.modules[module.name] = module

    def register_modules(self, modules: List[AsyncUnshortenModule]):
        for module in modules:
            self.register_module(module)

    async def unshorten(
        self,
        uri: str,
        module: str = None,
        timeout: int = None,
        unshorten_nested: bool = False,
        force: bool = False,
    ) -> str:

        timeout = timeout or self._default_timeout

        if module and module in self.modules:
            return await self.modules[module].unshorten(uri)

        if unshorten_nested:
            last_uri = uri
            while True:
                matched = False
                for k, m in self.modules.items():
                    if m.is_match(uri):
                        matched = True
                        uri = await m.unshorten(uri)
                        if uri == last_uri:
                            break
                        last_uri = uri
                if not matched:
                    break
        else:
            for k, m in self.modules.items():
                if m.is_match(uri):
                    return await m.unshorten(uri)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=uri,
                headers=self._default_headers,
                timeout=timeout,
                allow_redirects=True,
            ) as response:
                return str(response.url)
