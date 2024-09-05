import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic_spider'
    
    # 크롤링할 기본 URL을 지정합니다.
    start_urls = ['https://ko.wikipedia.org/wiki/%EC%9E%90%EC%97%B0']  

    def parse(self, response):
        self.log(f'Visited {response.url}')
        
        title = response.xpath('//title/text()').get()
        self.log(f'Title: {title}')
