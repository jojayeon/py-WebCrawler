import scrapy
from urllib.parse import urlencode, urlparse, parse_qs
from scrapy.http import Request
from collections import defaultdict

class NewsSpiderSpider(scrapy.Spider):
    name = "search_spider"
    allowed_domains = ["yna.co.kr"] 
    
    def __init__(self, query=None, search_terms=None, *args, **kwargs):
        super(NewsSpiderSpider, self).__init__(*args, **kwargs)

        self.query = query 
        self.search_terms = (search_terms or "").split(",")  

        self.total_count = defaultdict(int)
        self.num_results = 50 

        # 검색 URL 생성
        params = {'q': self.query, 'num': str(self.num_results)}
        self.start_urls = [f"https://www.yna.co.kr/search/index?{urlencode(params)}"]
        
    def start_requests(self):
        headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        links = response.xpath('//a[contains(@href, "news.daum.net")]/@href').getall()

        for link in links:
            links = response.xpath('//a/@href').getall()
            for link in links:
                if '/view/' in link:
                    yield Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        article_content = ''.join(response.xpath('//p//text() | //div//text() | //article//text()').getall())
        article_content = ' '.join(article_content.split())

        results = self.analyze_content(article_content)
        for term, count in results.items():
            self.total_count[term] += count
            self.log(f"'{term}' 단어의 발생 횟수: {count} (URL: {response.url})")

    def analyze_content(self, content):
        found_terms = defaultdict(int)
        for term in self.search_terms:
            found_terms[term] += content.lower().count(term.lower())
        return found_terms

# 스파이더 마무리 끝
    def closed(self, reason):
        self.log(f"스파이더가 종료되었습니다. 종료 이유: {reason}")
        self.log(f"\n'{self.query}'에 관한 총 발생 횟수:")
        for term, count in self.total_count.items():
            self.log(f"'{term}': {count}")