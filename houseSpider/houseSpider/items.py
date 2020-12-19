# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousespiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    avg_price = scrapy.Field()
    detail_info = scrapy.Field()
    address = scrapy.Field()
    sell_point = scrapy.Field()
    img_url = scrapy.Field()
