# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class HousespiderPipeline:
    # Just execute once before crawling
    def open_spider(self, spider):
        if spider.name == 'anjuke':
            self.f = open("anjuke_data.txt", 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if spider.name == 'anjuke':
            self.f.write(json.dumps(dict(item), ensure_ascii=False, indent=2) + ',\n')

    # Just execute once before spider closed
    def close_spider(self, spider):
        if spider.name == 'anjuke':
            self.f.close()
