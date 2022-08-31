import re
import copy
import asyncio
import json
import aiohttp


from async_unshortenit.module import AsyncUnshortenModule
from async_unshortenit.exceptions import AsyncUnshortenFailed


class ShorteSt(AsyncUnshortenModule):

    name = "shortest"
    domains = ["sh.st", "festyy.com", "ceesty.com"]

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    async def unshorten(self, uri: str) -> str:
        res_text, res_url = await self.get(uri)

        session_id = re.findall(r"sessionId\:(.*?)\"\,", res_text)
        if len(session_id) == 0:
            raise AsyncUnshortenFailed("No sessionId variable found.")

        if len(session_id) > 0:
            session_id = re.sub(r"\s\"", "", session_id[0])

            http_header = copy.copy(self.headers or {})
            http_header["Content-Type"] = "application/x-www-form-urlencoded"
            http_header["Host"] = "sh.st"
            http_header["Referer"] = uri
            http_header["Origin"] = "http://sh.st"
            http_header["X-Requested-With"] = "XMLHttpRequest"

            await asyncio.sleep(5)

            payload = {"adSessionId": session_id, "callback": "c"}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://sh.st/shortest-url/end-adsession",
                    params=payload,
                    headers=http_header,
                    timeout=self.timeout,
                ) as r:
                    response = (await r.text())[6:-2]
                    if r.status == 200:
                        resp_uri = json.loads(response)["destinationUrl"]
                        if resp_uri is not None:
                            uri = resp_uri
                        else:
                            raise AsyncUnshortenFailed("Error extracting url.")
                    else:
                        raise AsyncUnshortenFailed("Error extracting url.")

        return uri
