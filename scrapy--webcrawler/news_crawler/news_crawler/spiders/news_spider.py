import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic_spider'
    
    def __init__(self, search_term='', *args, **kwargs):
        super(BasicSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term
        self.start_urls = [
            f'https://www.chosun.com/search?query={search_term}',
            # f'https://search.joongang.co.kr/search?q={search_term}',
            f'https://search.hani.co.kr/Search?query={search_term}',
            # f'https://search.kyunghyang.com/search?q={search_term}',
            f'https://search.daum.net/search?w=news&lpp=10&DA=STC&rtmaxcoll=1&q={search_term}'
        ]

    def parse(self, response):
        self.log(f'Visited {response.url}')
        
        # 모든 <a> 태그의 href 속성을 추출하여 리스트로 가져옵니다.
        links = response.xpath('//a/@href').getall()
        
        # 추출한 링크들을 로그로 출력합니다.
        print(f'\nLinks found on {response.url}:')
        for link in links:
            print(link)
        
        # 검색어를 로그로 출력합니다.
        self.log(f'Search Term: {self.search_term}')
