# import scrapy


# class NewsSpiderSpider(scrapy.Spider):
#     # 고유 이름
#     name = "news_spider"
#     # 크롤링할  도메인
#     allowed_domains = ["example.com"]
#     # 크롤링 시작한 url 목록
#     start_urls = ["https://example.com"]
#     # 응답을 처리하고 데이터를 추출하는 로직
#     def parse(self, response):
#         pass

import scrapy
from urllib.parse import urlencode, urlparse, parse_qs
from scrapy.http import Request
from collections import defaultdict

class NewsSpiderSpider(scrapy.Spider):
    name = "search_spider"
    allowed_domains = ["google.com"]
    
    def __init__(self, query=None, search_terms=None, *args, **kwargs):
        super(NewsSpiderSpider, self).__init__(*args, **kwargs)
        self.query = query or "저출산"  # 기본 검색어
        self.search_terms = (search_terms or "").split(",")  # 쉼표로 구분된 문자열을 리스트로 변환
        self.total_count = defaultdict(int)
        self.num_results = 50  # 기본 결과 수

        # 검색 URL 생성
        params = {'q': self.query, 'num': str(self.num_results)}
        self.start_urls = [f"https://www.google.com/search?{urlencode(params)}"]

    def parse(self, response):
        # 구글 검색 결과에서 URL 추출
        links = response.xpath('//a/@href').getall()
        for link in links:
            if 'url?q=' in link and 'webcache' not in link:
                parsed_link = parse_qs(urlparse(link).query)
                url = parsed_link.get('q', [None])[0]
                if url:
                    yield Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        # 기사에서 텍스트 추출 및 분석
        article_content = ''.join(response.xpath('//p//text() | //div//text() | //article//text()').getall())
        article_content = ' '.join(article_content.split())

        # 검색어 분석
        results = self.analyze_content(article_content)
        for term, count in results.items():
            self.total_count[term] += count
            self.log(f"'{term}' 단어의 발생 횟수: {count} (URL: {response.url})")

    def analyze_content(self, content):
        found_terms = defaultdict(int)
        for term in self.search_terms:
            found_terms[term] += content.lower().count(term.lower())
        return found_terms

    def closed(self, reason):
        # 크롤링이 완료되면 총 단어 발생 횟수 출력
        self.log(f"\n'{self.query}'에 관한 총 발생 횟수:")
        for term, count in self.total_count.items():
            self.log(f"'{term}': {count}")
