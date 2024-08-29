import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
# 구글
# https://www.google.com/
# https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results}

def get_search_results(query, num_results):
    # 주소
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results}"#변환 주소처럼
    #봇인거 걸리지 말아줘
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        #요청
        response = requests.get(search_url, headers=headers)
        #요청 확인
        response.raise_for_status()
        # html파싱 객체로
        soup = BeautifulSoup(response.text, 'html.parser')
        # 구글 검색 결과에서 URL 추출
        links = []
        # a태그에서 주소 찾기 
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            print(href)
            if 'url=' in href:
                link = href.split('url=')[1].split('&')[0]
                print(link)
                #주소에 맞게 디코딩
                links.append(urllib.parse.unquote(link))
        return links
    #오류
    except requests.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return []

def crawl_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # 기사 내용 수집
        article_content = ''
        #가져올 기사들의 내용이 있는 태그들 
        tags_to_extract = ['p', 'div', 'article', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'li','span','a']
        #추출
        for tag in tags_to_extract:
            for element in soup.find_all(tag):
                article_content += element.get_text() + ' '
        return article_content
    except requests.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return None

def analyze_content(content, search_terms):
    found_terms = {term: 0 for term in search_terms}
    for term in search_terms:
        found_terms[term] = content.lower().count(term.lower())
    return found_terms


# 실행파트 - 이 파일에서만 작동하는 코드이다 - export 해서 다른 파일에서 실행했을 때__name__가 있는 부분은 실행되지 않는다. 이 주석 아래부분은 export했을 때 없는 부분이라 생각하면 됨 
if __name__ == "__main__":
    query = "고령화" #검색어 
    search_terms = ["고령화","저출산"] #분석화할 데이터
    # 구글에서 검색 결과 URL 추출
    search_results = get_search_results(query,5)
    if search_results:
        print("검색된 URL 목록:")
        print("search_results")
        for url in search_results:
            print(url)  # URL 출력
    # 각 URL에서 내용 크롤링 및 분석
    for url in search_results:
        #크롤링
        print(f"\n크롤링 중인 URL: {url}")
        content = crawl_article(url)
        if content:
            #내용확인
            # print("크롤링된 내용의 일부:")
            # print(content[:100])  # 크롤링된 내용의 처음 500자 출력 (길이가 길 경우 확인용)
            #분석 횟수 계산
            results = analyze_content(content, search_terms)
            for term, count in results.items():
                print(f"'{term}' 단어의 발생 횟수: {count}")
        else:
            print("크롤링된 내용이 없습니다.")
        
        time.sleep(1)
