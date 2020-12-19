import os
import time
import random
import requests
import json
from lxml import etree
from fake_useragent import UserAgent


headers = {}
url = 'https://movie.douban.com/top250'
        

class VideoSpider:
    def __init__(self, url, headers, max_num=-1, verbose=False, output=None):
        self._headers = headers
        self._useragents = []
        self.contents = []
        self.start_url = url
        self.urls = [url]
        self.verbose = verbose
        self.spide_pages = 0
        self.max_num = max_num
        self.spide_stop = False
        self.output = output if output else "output_json.text"

    def setup(self):
        if os.path.exists(self.output):
            os.remove(self.output)
        
        self._config_ua()
        
    def _config_ua(self):
        ua = UserAgent()
        for _ in range(10):
            self._useragents.append(ua.random)
        
    def download(self, url):
        headers=self._headers
        headers['User-Agent'] = random.choice(self._useragents)
        try:
            res = requests.get(url, headers=headers)
            htmlstr = res.content.decode()
            html = etree.HTML(htmlstr)
            return html
        except Exception as e:
            raise(e)

    def parser(self, html, out_file=None):
        li_list = html.xpath('//*[@id="content"]/div/div[1]/ol/li')
        
        if li_list:
            for li in li_list:
                title = li.xpath('./div/div[2]/div[1]/a/span[1]/text()')
                detail_url = li.xpath('./div/div[2]/div[1]/a/@href')
                playable = True if li.xpath('./div/div[2]/div[1]/span/text()') else False
                desc = li.xpath('./div/div[2]/div[2]/p[1]/text()')
                rating_num = li.xpath('./div/div[2]/div[2]/div/span[2]/text()')
                assessment = li.xpath('./div/div[2]/div[2]/div/span[4]/text()')
                quote = li.xpath('./div/div[2]/div[2]/p[2]/span/text()')
                
                item = {}
                item['title'] = title[0].strip() if title else ''
                item['detail_url'] = detail_url[0].strip() if detail_url else ''
                item['desc'] = desc[0].strip() if desc else ''
                item['rating_num'] = rating_num[0].strip() if rating_num else '0'
                item['assessment'] = assessment[0].strip() if assessment else ''
                item['quote'] = quote[0].strip() if quote else ''
                
                if playable and item['detail_url']:
                    time.sleep(2)
                    html = self.download(item['detail_url'])
                    item['video_url'] = self.parse_detail(html)

                self.contents.append(item)
                if self.verbose:
                    print(item)

                if out_file:
                    out_file.write(json.dumps(item, ensure_ascii=False, indent=2) + ',\n')
                
                if len(self.contents) >= self.max_num:
                    self.spide_stop = True
                    print("Reach to max spiding number. Stop crawling")
                    return
        else:
            print("Empty list")


    def parse_detail(self, html):
        li_list = html.xpath('//*[@id="content"]/div[3]/div[2]/div[1]/ul/li')
        video_list = []
        for li in li_list:
            link = li.xpath('./a/@href')[0].strip()
            if link:
                video_list.append(link)
        return video_list
    
    
    def crawl(self):
        self.setup() # Delete old output file, generate user_agents

        while self.urls and not self.spide_stop:
            url = self.urls.pop(0)
            print("Spiding url: " + url)
            
            self.spide_pages += 1
            out_file = open(self.output, 'a', encoding='utf-8')
            html = self.download(url)
            self.parser(html, out_file)
            out_file.close()            
            print("Finished spiding pages: ", self.spide_pages)
    
            next_page = html.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href')
            if next_page:
                self.urls.append(self.start_url + next_page[0].strip())
            
            time.sleep(random.randint(3,6))


if __name__ == "__main__":
    spider = VideoSpider(url, headers, max_num=250)
    spider.crawl()

