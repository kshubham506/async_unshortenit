from lxml import html
from urllib.parse import urljoin



from module import AsyncUnshortenModule
from exceptions import AsyncUnshortenFailed


class MetaRefresh(AsyncUnshortenModule):

    name = "meta-refresh"
    domains = ["href.li", "anonymz.com"]

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    async def unshorten(self, uri: str) -> str:
        res_text, resp_url = await self.get(uri)

        html_tree = html.fromstring(res_text)
        meta_attr = html_tree.xpath(
            "//meta[translate(@http-equiv, 'REFSH', 'refsh') = 'refresh']/@content"
        )
        if not meta_attr:
            raise AsyncUnshortenFailed("No meta refresh tag present.")

        _, url = meta_attr[0].split(";")
        if url.strip().lower().startswith("url="):
            url = url[5:]
            if not url.startswith("http"):
                url = urljoin(resp_url, url)

            return url
        else:
            raise AsyncUnshortenFailed("Failed to extract meta refresh tag.")
