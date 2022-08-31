
from module import AsyncUnshortenModule

class Redirect(AsyncUnshortenModule):

    name = "redirect"
    domains = set(["fb.me"])

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    async def unshorten(self, uri: str) -> str:
        res_text, url = await self.get(uri)
        return url
