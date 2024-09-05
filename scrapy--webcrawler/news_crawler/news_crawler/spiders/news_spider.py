import scrapy
from urllib.parse import urlencode, urlparse, parse_qs
from scrapy.http import Request
from collections import defaultdict

class NewsSpiderSpider(scrapy.Spider):
    name = "search_spider"
    allowed_domains = ["yna.co.kr"] 
    
    # __init__클래스의 생성자 메서드 - 인자 이어받기
    # query,search_terms매개변수인데 기본값을 None으로 설정함 
    # *args - list모든 걸 가져온다.
    # **kwargs - 딕셔너리 형태의 모든 인자들 가져온다.
    def __init__(self, query=None, search_terms=None, *args, **kwargs):
        # super() - 자식 클래스가 부모 클래스 부르기
        # NewsSpiderSpider인 부모 클래스의 인자를 물려 받는 구조
        #  *args, **kwargs를 물러받음 
        super(NewsSpiderSpider, self).__init__(*args, **kwargs)

        self.query = query # or "저출산" 무조건 정해줄 것이라 제외   # 기본 검색어
        self.search_terms = (search_terms or "").split(",")  # 쉼표로 구분된 문자열을 리스트로 변환

        # collections 모듈에 
        # defaultdict(int) - 딕셔너리로 반환 존재하지 않는 키에 접근하면 0으로 반환
        self.total_count = defaultdict(int)
        self.num_results = 50  # 기본 결과 수

        # 검색 URL 생성
        params = {'q': self.query, 'num': str(self.num_results)}
        # 크롤링항 주소 
        # print(params)
        self.start_urls = [f"https://www.yna.co.kr/search/index?{urlencode(params)}"]
        # print(self.start_urls)
        
    # User-Agent를 명시적으로 추가하여 요청할 수 있습니다.
    # start_requests 메서드에서 각 요청에 대해 헤더 설정을 추가함
    def start_requests(self):
        headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # start_urls에서 설정한 검색 URL로 요청을 보낼 때, User-Agent를 헤더에 포함
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        # 구글 검색 결과에서 URL 추출
        # scrapy의 response.xpath() 메서드
        # '//a/@href' - a태그에 href 주소를 가져와라 
        # .getall() 모든 요소를 달란는 뜻 - list형식으로 달라 
        links = response.xpath('//a[contains(@href, "news.daum.net")]/@href').getall()

        for link in links:
            # 이건 변경이 조금 있어야 할 듯 url?q=이 무조건 있어야하고 webcache라는 문자열이 있으면 가져오지 말라는 조건인데 왜 있냐? 
            # //! 변경해야할 듯 내가 원하는 형태가 아님 
            links = response.xpath('//a/@href').getall()
                # urlparse url 구성요소를 나누는 역할
                    # 종류별로 나누는데 - .query부분만 가져오길 원하는 형태임
                # .query
                #  ParseResult 객체 반환
                    # ParseResult 객체 - urllib.parse 모듈에서 urlparse 함수가 반환하는 객체
                # urllib.parse 모듈 - parse_qs() 딕셔너리 형태로 변경
                # 결론 link 주소들을 나누어서 뒷부부만 가져온 것을 딕셔너리 구조로 병경해서 대입한다.
                # //todo parsed_link = parse_qs(urlparse(link).query)
                # get() 딕셔너리의 값만 추출
                # 기본값으로 none으로 처리했고 q가 있으면 통과 되게 설정 
                # parsed_link에 첫번째 요소 가져와서 
                # //todo url = parsed_link.get('q', [None])[0]
            for link in links:
                if '/view/' in link:
                # if url:
                    # Scrapy - yield를 사용하여 데이터나 요청을 생성한다. - 특이하게 제너레이터 함수에서 값을 반화하는데 사용
                    # Request - Scrapy에서 새로운 웹 요청을 생성하는 객체
                    # url은 앞에 설정해 놓은 url 사용
                    # callback 내가 아는 콜백으로 함수 parse_article을 불러와서 전처리 과정을 한다.
                    # yield Request(url=url, callback=self.parse_article)
                    yield Request(url=link, callback=self.parse_article)
                    # yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        # 기사에서 텍스트 추출 및 분석
        # 데이터 가져온 것들 각 태그별로 정리되어 있는 것들 
        # .getall() - 가져온다.
        # join() - 자스는 뒤에 .join('')안에서 정해주는 방면
        # join() - 파이썬은 앞에서 ''.join()으로 앞에서 정해줌
        # //! 지금 p, div ,article 3가지만 있기 때문에 정보의 다양성이 떨어질 것으로 예상됨 - 따라서 추가 예정
        article_content = ''.join(response.xpath('//p//text() | //div//text() | //article//text()').getall())
        # split() - 공백을 기준으로 나누기 
        # ' '.join() 으로 한 칸 띄어쓰기한 형태의 구조로 변경
        article_content = ' '.join(article_content.split())

        # 검색어 분석

        results = self.analyze_content(article_content)
        # items으로 키와 값을 모두 주는 형태
        for term, count in results.items():
            # 총 갯수 계산
            self.total_count[term] += count
            # self.log(f"'{term}' 단어의 발생 횟수: {count} (URL: {response.url})")

    def analyze_content(self, content):
        # 딕셔너리구조로 키없으면 0 으로
        found_terms = defaultdict(int)
        for term in self.search_terms:
            # 영어일 수 있으니까 소문자 처리
            found_terms[term] += content.lower().count(term.lower())
        return found_terms

# 스파이더 마무리 끝
    def closed(self, reason):
        # 크롤링이 완료되면 총 단어 발생 횟수 출력
        # self.log(f"스파이더가 종료되었습니다. 종료 이유: {reason}")
        # self.log(f"\n'{self.query}'에 관한 총 발생 횟수:")
        for term, count in self.total_count.items():
            # self.log(f"'{term}': {count}")
            print("A")