import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic_spider'
    
    # 크롤링할 기본 URL을 지정합니다.
    start_urls = [
        'https://www.chosun.com/',
        'https://www.joongang.co.kr/',
        'https://www.hani.co.kr/',
        'https://www.kyunghyang.com/',
        'https://www.yna.co.kr/',
        'https://news.daum.net/'
        # 조선
        # 중앙
        # 한겨레
        # 경향
        # 연합
        # 다음
    ]
    
    def __init__(self, search_term='', *args, **kwargs):
        super(BasicSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term

    def parse(self, response):
        self.log(f'Visited {response.url}')
        
        # 제목을 추출합니다.
        title = response.xpath('//title/text()').get()
        self.log(f'Title: {title}')

        # 검색어를 로그로 출력합니다.
        self.log(f'Search Term: {self.search_term}')