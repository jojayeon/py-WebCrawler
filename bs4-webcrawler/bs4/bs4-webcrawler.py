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
            if 'url=' in href:
                link = href.split('url=')[1].split('&')[0]
                if not ('.jpg' in link or '.png' in link or '.gif' in link or '.pdf' in link or '.mp4' in link or 'vimeo.com' in link or 'instagram.com' in link or 'imgur.com' in link or 'download' in link or 'attachment' in link or 'down.do' in link or 'FileDown.do' in link or 'google.com' in link or 'youtube.com' in link) and ('http' in link or 'https' in link):
                    links.append(urllib.parse.unquote(link))
                #주소에 맞게 디코딩
        return links
    #오류
    except requests.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return []

def extract_text_from_tag(tag):
    text = ''
    for element in tag.contents:
        if isinstance(element, str):
            text += element.strip() + ' '
    return text.strip()

def crawl_article(url):
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # 기사 내용 수집
        article_content = ''
        tags_to_extract = [
    'p', 'div', 'article', 'section', 'header', 'footer', 'nav', 'aside',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'code',
    'li', 'a', 'summary','span','strong','td']
        for tag_name in tags_to_extract:
            for tag in soup.find_all(tag_name):
                # 자신의 텍스트만 추출
                article_content += extract_text_from_tag(tag) + ' '
                
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
    query = "저출산" #검색어 
    search_terms = ["산업화","도시화","지원","의료","수명","평균 수명","해결","문제","연금","임금","병원","비용","노동력","노동","생산","일자리","노인일자리","정년","사교육","이성","비용","데이트","시간","여유","결혼","나이","자녀","딩크족","안정감","경력","경력단절","커리어","불임","입양","육아","양육","결혼율","열등감","경쟁사회","sns","연예인","고령화"] #분석화할 데이터
    # 구글에서 검색 결과 URL 추출
    search_results = get_search_results(query,50) #가져올 사이트 갯수 적기
    total_count = {term: 0 for term in search_terms}
    if search_results:
    # 각 URL에서 내용 크롤링 및 분석
        for url in search_results:
        #크롤링
            print(f"\n크롤링 중인 URL: {url}")
            content = crawl_article(url)
            if content:
                #분석 횟수 계산
                results = analyze_content(content, search_terms)
                for term, count in results.items():
                    print(f"'{term}' 단어의 발생 횟수: {count}")
                    total_count[term] += count
            else:
                print("크롤링된 내용이 없습니다.")
            time.sleep(0.3) 
    print(f"\n ${query}에 관한 총 발생 횟수:")
    for term, count in total_count.items():
        print(f"'{term}': {count}")
        
# 고령화
# ["산업화","도시화","현대화","지원","의료","수명","평균 수명","해결","문제","연금","임금","병원","비용","노동력","노동","생산","일자리","노인일자리","시간","여유","결혼","나이","자녀","육아","양육","초저출산","저출산"]
# 저출산
# ["산업화","도시화","지원","의료","수명","평균 수명","해결","문제","연금","임금","병원","비용","노동력","노동","생산","일자리","노인일자리","정년","사교육","이성","비용","데이트","시간","여유","결혼","나이","자녀","딩크족","안정감","경력","경력단절","커리어","불임","입양","육아","양육","결혼율","열등감","경쟁사회","sns","연예인","고령화"]