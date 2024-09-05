import scrapy
from urllib.parse import urljoin

class BasicSpider(scrapy.Spider):
    name = 'basic_spider'
    
    def __init__(self, search_term='', *args, **kwargs):
        super(BasicSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term
        self.start_urls = [
            f'https://www.chosun.com/search?query={search_term}',
            f'https://search.hani.co.kr/Search?query={search_term}',
            f'https://search.daum.net/search?w=news&lpp=10&DA=STC&rtmaxcoll=1&q={search_term}'
        ]

    def parse(self, response):
        self.log(f'Visited {response.url}')
        
        # 모든 <a> 태그의 href 속성을 추출하여 리스트로 가져옵니다.
        links = response.xpath('//a/@href').getall()
        
        # 추출한 링크들을 로그로 출력합니다.
        filtered_links = ['google.com']

        for link in links:
            full_url = urljoin(response.url, link)  # 상대 URL을 절대 URL로 변환
            # //! if full_url.startswith('http') and not any(excluded in full_url for excluded in self.exclude_strings): 문제 있음 
            filtered_links.append(full_url)

        # 필터링된 링크를 로그에 기록합니다.
        for url in filtered_links:
            self.log(f'Filtered URL: {url}')
