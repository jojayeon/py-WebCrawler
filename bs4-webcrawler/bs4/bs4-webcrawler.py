import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from collections import Counter
import re

# 제외할 단어 리스트
# 저출산일 경우의 단어 필터링
EXCLUDE_WORDS = [ '은', '는', '이', '가', '께서', '이란', '란', '이니까', '는가','이도', '도', '라도', '밖에', '말고', '의', '의가', '이어', '로서','이면서', '이기 때문에', '와', '과', '부터', '에', '가지고', '로','처럼', '같이', '의해', '으로', '하여', '기 때문에', '뿐이다', '보다','하니', '라는', '냐고', '게', '때문에', '이라면', '이로', '이라서','든지', '또는', '뿐만 아니라', '까지', '로써', '대해서', '이래서', '이자','이기도 하고', '가치', '에도', '하니까', '하더라도', '관해서', '향해서','이해', '하고서', '와 함께', '과 더불어', '이후', '또한', '의하', '에 대한','하여서', '마치', '하기에', '만큼', '따라서', '같은', '지','해도', '하게', '이로서', '이처럼', '한테', '언제', '라고도', '다시', '과도','와도', '그러나', '자체', '단', '조차', '대해', '저', '한테서', '예를 들어', '뿐', '정도', '게다가', '이야', '없이', '더라도', '하기 위해', '자', '씩', '여', '그것', '상황에서','달리', '안에', '을','를', '에 의해서','의해서', '지라도', '한편', '관련해서','각','각각','위해', '말하자면', '따라', '비해', '반해', '이후에', '따르다','다만', '의 경우', '및', '조차도', '에 비해', '에 따라', '왜냐하면', '미래','라든지', '물론', '여기', '무엇', '어디', '어떤', '그렇게', '이렇게','왜', '어떻게','있고','인해','동일','산업','것이','젊은',

'크게','이에','그리고','비율이','이러한','한다','한','사회의','인한','더','큰','있다','수','하는','등','등을','지역','등의','확대','변화','있으며','활성화','사회','전체','중','세','이상','차지하는','우리나라의','년에','년에는','것으로','년','현재','예상된다','전','빠르게','한국은','위한','명','명으로','증가할','대한','할','높은','에서','명이','있는','우리나라는','특히','사회적','통해','세계에서','될','영향을','것이다','따른','후','내용','있습니다','있을','경우','선택','다운로드','팝업','타이틀','끝','버튼','관련','라벨','본','내용은','해당','건강','다른','이동','문제','임시','이용','닫기','정보','문의','안내','수정','시','전체메뉴','세종','본문','바로가기','역사','정치','인물','현황','메뉴','다음','이전','사용','문서','최근','평균','된다','많은','때','대한민국','한국의','다양한','가장','많이','결과','문제가','모든','여러','연구','매우','억','적용되어','대한민국의','비율','월','기준','거의','자세한','년부터','국가','그','국가가','빠른','대','낮은','일본은','한국','약','이미','것이라고','따르면','만','일','이는','세계','없는','주요','중국','미국','년대','프랑스','영국','유럽','일본','편집','변경','개요','보기','추가','서비스','분석','태그','조회','상승','배','모두','일반','등록','국제','이유','개인정보처리방침','소개','정책','검색','로그인','개','기사','광고','컨텐츠','댓글','공지사항','영역','뉴스','안','만에','내','말했다','우측','사진','더보기','응급실','전체보기','첫','대표','하락','추천','함께','적용','운영','관심','원','호','구독','클래스','중고','장바구니','대여','스웨덴','열기','우리나라','중심으로','기타','논문','개국','인용','값','편집패널','페이지','디지털','저자','통권','한국은행','프로그램','있음','구분','상품','있어요','지역본부','통화정책','금융안정','경제교육','리뷰','이벤트','핫트랙스','조건','리스트형','썸네일형','스크립트','버튼영역','상품명','부제명','출판사','가격정보','판매중일떄','교보일때','종이책','컬쳐유료','일때','핫트랙스일때','판매중이','아닐떄','장터일때','찜하기','썸네일로','타입에서','노출되는','케이스','관칭관제','가이드','참고','부탁드립니다','부가','인물역할코드인물코드인물명인물역할코드인물코드인물명','모두보기','저자에','인물역할코드','좋아요','버튼썸네일','레이아웃','클로버리뷰','클로버','결제기능','캐스팅일때','판매중예약중','일떄','앨범','아닐경우','쿠폰이','있을때','소장','상품만','연관상품','아닐때','체크박스','바로드림','타입','임시조건','국내도서','상품선택','저자글','바로구매','기관']
# 여기에 제외할 단어들을 추가하세요

def get_search_results(query, num_results):
    # 구글에 원하는 단어로 검색 몇개 검색할지 정해줌 
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results}"
    # 봇이 아닌 것처럼 만들어줌
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        # get요청을 보냄
        response = requests.get(search_url, headers=headers)
        # 요청 실패시 404에러
        response.raise_for_status()
        # text데이터 파싱 BeautifulSoup객체
        soup = BeautifulSoup(response.text, 'html.parser')
        # 주소들 넣은 list 빈공간
        links = []
        # a태크에 주소 있는 부분 모두 가져와서 하나하나 순서대로  a_tag로 주면서 for문처럼하나씩 작업
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if 'url=' in href:
                # 주소 전처리 
                    # url= ~ & 사이에 있는 문자열 
                link = href.split('url=')[1].split('&')[0]
                # 주소들 필터링
                if not ('.jpg' in link or '.png' in link or '.gif' in link or '.pdf' in link or '.mp4' in link
                        or 'vimeo.com' in link or 'instagram.com' in link or 'imgur.com' in link or 'download' in link or 'attachment' in link or 'down.do' in link or 'FileDown.do' in link or 'google.com' in link or 'youtube.com' in link) and ('http' in link or 'https' in link):
                    # 디코딩 
                    links.append(urllib.parse.unquote(link))
        return links
    except requests.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return []

# 태그에 하위에 있는 문자열만 가져오게 만듬 중복 때문에
def extract_text_from_tag(tag):
    text = ''
    # tag안에 자료 모두 한번 씩 element로 넣음
    for element in tag.contents:
        # isinstance - bs4의 함수 -> element안에 str만 찾음 
        if isinstance(element, str):
            #element str만 빼고 다 무시(strip)
            text += element.strip() + ' '
    # 한번더 공백이 존재할 수 있으니까 strip()
    return text.strip()

def crawl_article(url):
    try:
        # get요청인데 8초동안 처리 못하면 넘어감
        response = requests.get(url, timeout=8)
        # 에러 처리
        response.raise_for_status()
        # 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        article_content = ''
        # 데이터 가져올 태그들
        tags_to_extract = [
            'p', 'div', 'article', 'section', 'header', 'footer', 'nav', 'aside',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'code',
            'li', 'a', 'summary', 'span', 'strong', 'td'
        ]
        # tags_to_extract 태그들 tag_name으로 순차적으로 대입
        for tag_name in tags_to_extract:
            # soup 가져온 데이터에서 맞는 태그를 찾음 그리고 tag에 넣음
            for tag in soup.find_all(tag_name):
                # extract_text_from_tag(tag)실행해서 결과를 article_content에 저장 
                article_content += extract_text_from_tag(tag) + ' '
        return article_content
    except requests.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return None

# 단어 별로 모으기 위해서 
def preprocess_text(text):
    # 혹시 모르는 영어 소문자로 변환
    text = text.lower()
    # 한글과 공백을 제외한 모든 문자를 제거
    text = re.sub(r'[^가-힣\s]', '', text)
    # 연속된 공백을 단일 공백으로 변환
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_words(text):
    # 공백 한번 더 제거 전처리과정에서 생기는 공백을 제거하기 위해서 
    words = text.split()
    return words


def analyze_content(content):
    preprocessed_text = preprocess_text(content)
    words = extract_words(preprocessed_text)
    # Counter 단어별로 몇번 나왔는지 카운트 
    word_counts = Counter(words)
    return word_counts

# word_counts단어들 , min_count 최소 갯수 , exclude_words제외할 단어
def filter_words(word_counts, min_count, exclude_words):
    # 제외할 단어 리스트를 포함하여 필터링
    # min_count보다 큰경우만 찾아, word 안에 exclude_words이 단어들이 없어야 한다.는 조건을 걸려있음
    # word-키, count-값 으로 저장한 딕셔너리로 저장 
    filtered_counts = {word: count for word, count in word_counts.items() if count >= min_count and word not in exclude_words}
    return filtered_counts

# 외부에서 실행되지 않게 설정
if __name__ == "__main__":
    query = "고령화"
    # 고령화을 단어로 50개 검색
    search_results = get_search_results(query, 50)
    # 전체 단어 빈도수 
    total_word_counts = Counter()
    
    if search_results:
        for url in search_results:
            # 크롤링한 url표기
            print(f"\n크롤링 중인 URL: {url}")
            # 캐그별로 분류된 데이터
            content = crawl_article(url)
            if content:
                # 단어 카운트
                word_counts = analyze_content(content)
                # 
                total_word_counts.update(word_counts)
            else:
                print("크롤링된 내용이 없습니다.")
            time.sleep(0.5)
    
    # 다 하고 나서 원하는 데이터만 가져오게 설정 
    # 빈도수가 20번 이상인 것들만 가져오고 필터링
    min_count = 20
    filtered_word_counts = filter_words(total_word_counts, min_count, EXCLUDE_WORDS)
    
    print(f"\n{query}에 관한 총 단어 발생 횟수 ({min_count}회 이상):")
    # .items() 모든 키-값 쌍 word-키, count-값 으로 할당
    for word, count in filtered_word_counts.items():
        print(f"'{word}': {count}")
    
