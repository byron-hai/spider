import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['https://haokan.baidu.com/tab/yinyue']

    def parse(self, response):
        li_list = response.xpath('//*[@id="rooot"]/div[2]/div[3]/div/div/ul/li').extract()
        print(len(li_list))
