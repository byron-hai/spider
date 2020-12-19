import scrapy
import time
from houseSpider.items import HousespiderItem


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://beijing.anjuke.com/sale/?from=navigation#']

    def parse(self, response):
        li_list = response.xpath('//*[@id="houselist-mod-new"]/li')
        for li in li_list:
            item = HousespiderItem()
            # li.xpath is relative xpath
            item['title'] = li.xpath('./div[2]/div[1]/a/@title').extract_first()
            detail_url = li.xpath('./div[2]/div[1]/a/@href').extract_first()
            item['img_url'] = li.xpath('./div[1]/img/@src').extract_first()
            item['detail_info'] = li.xpath('./div[2]/div[2]/span/text()').extract()  # extrct all
            item['address'] = li.xpath('./div[2]/div[3]/span/@title').extract_first()
            item['price'] = li.xpath('./div[3]/span[1]/strong/text()').extract_first() + \
                            li.xpath('./div[3]/span[1]/text()').extract_first()
            item['avg_price'] = li.xpath('./div[3]/span[2]/text()').extract_first()

            if detail_url:
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta=item)

        time.sleep(2)
        #
        # # Next Page
        try:
            next_url = response.xpath('//*[@class="aNxt"]/@href').extract_first()
            yield scrapy.Request(next_url, callback=self.parse)
        except Exception as e:
            print(e)

    def parse_detail(self, response):
        item = response.meta
        item['sell_point'] = response.xpath('//*[@class="houseInfo-item"][1]/div/span/text()').extract()
        yield item
