from scrapy import Spider
from scrapy.crawler import CrawlerProcess

from ..models.beer import Beer


class Tesco(Spider):
    name = "tesco_spider"
    start_urls = ["https://nakup.itesco.cz/groceries/cs-CZ/shop/alkoholicke-napoje/pivo/all"]

    def parse(self, response, **kwargs):
        for item in response.xpath("//li[contains(@class, 'product-list--list-item')]"):
            link = item.xpath(".//a[@data-auto='product-tile--title']/@href").get()
            title = item.xpath(".//a[@data-auto='product-tile--title']/text()").get()

            price = float(
                item.xpath(".//div[contains(@class, 'price-per-sellable-unit')]//span[@data-auto='price-value']/text()")
                .get()
                .replace(",", ".")
            )
            price_liter = float(
                item.xpath(
                    ".//div[contains(@class, 'price-per-quantity-weight')]//span[@data-auto='price-value']/text()"
                )
                .get()
                .replace(",", ".")
            )

            yield Beer(
                title=title,
                volume=price / price_liter,
                price=price,
                link=response.urljoin(url=link),
            )

        for next_page in response.xpath(
            "//li[@class='pagination-btn-holder']"
            "/a[@class='pagination--button prev-next' and ./span[@class='icon-icon_whitechevronright']]"
        ):
            yield response.follow(next_page, self.parse)

    @classmethod
    def run(cls):
        process = CrawlerProcess()
        process.crawl(cls)
        process.start()
