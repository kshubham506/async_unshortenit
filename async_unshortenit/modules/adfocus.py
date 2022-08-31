import re
import copy


from async_unshortenit.module import AsyncUnshortenModule
from async_unshortenit.exceptions import AsyncUnshortenFailed


class AdFocus(AsyncUnshortenModule):

    name = "adfocus"
    domains = set(["adfoc.us"])

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    async def unshorten(self, uri: str) -> str:
        orig_uri = uri
        res_text, url = await self.get(uri)

        adlink = re.findall("click_url =.*;", res_text)

        if len(adlink) == 0:
            raise AsyncUnshortenFailed("No click_uri variable found.")

        uri = re.sub('^click_url = "|"\;$', "", adlink[0])
        if re.search(r"http(s|)\://adfoc\.us/serve/skip/\?id\=", uri):
            http_header = copy.copy(self.headers)
            http_header["Host"] = "adfoc.us"
            http_header["Referrer"] = orig_uri

            res_text, url = await self.get(uri, headers=http_header)

            uri = url

        return uri
