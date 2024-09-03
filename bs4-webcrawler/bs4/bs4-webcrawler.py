import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from collections import Counter
import re

# 제외할 단어 리스트
EXCLUDE_WORDS = [ '은', '는', '이', '가', '께서', '이란', '란', '이니까', '는가',
    '이도', '도', '라도', '밖에', '말고', '의', '의가', '이어', '로서',
    '이면서', '이기 때문에', '와', '과', '부터', '에', '가지고', '로',
    '처럼', '같이', '의해', '으로', '하여', '기 때문에', '뿐이다', '보다',
    '하니', '라는', '냐고', '게', '때문에', '이라면', '이로', '이라서',
    '든지', '또는', '뿐만 아니라', '까지', '로써', '대해서', '이래서', '이자',
    '이기도 하고', '가치', '에도', '하니까', '하더라도', '관해서', '향해서',
    '이해', '하고서', '와 함께', '과 더불어', '이후', '또한', '의하', '에 대한',
    '하여서', '마치', '하기에', '만큼', '따라서', '같은', '지',
    '해도', '하게', '이로서', '이처럼', '한테', '언제', '라고도', '다시', 
    '과도','와도', '그러나', '자체', '단', '조차', '대해', '저', '한테서', 
    '예를 들어', '뿐', '정도', '게다가', '이야', 
    '없이', '더라도', '하기 위해', '자', '씩', '여', '그것', '상황에서',
    '달리', '안에', '을','를', '에 의해서','의해서', '지라도', '한편', '관련해서','각','각각',
    '위해', '말하자면', '따라', '비해', '반해', '이후에', '따르다',
    '다만', '의 경우', '및', '조차도', '에 비해', '에 따라', '왜냐하면', '미래',
    '라든지', '물론', '여기', '무엇', '어디', '어떤', '그렇게', '이렇게',
    '왜', '어떻게',
    
    '가능한','명을','되는','부족','점차','다양한','원인이','것이','특정','되었다','에서는','수','찾기','어렵다','주된','유배우','바','있다','경우','이러한','대부분','과거','대한','영국','년','아닌','주로','것을','세기','에','년부터','년까지','기간','동안','오히려','그','훨씬','여러','가진','가운데','높은','미국','만','때','따르면','사는','것으로','나타났다','이용한','년의','해당','지역','수가','이는','하는','한국과','국가의','중요한','내','간','등의','더','있는','반면','일부','현상이','영향','아시아','국가에서','년대','인해','크게','혹은','결과를','약','미치는','인한','영향을','자료','배','등으로','실제로','큰','반대로','상대적으로','이에','유럽','명','그리고','여전히','있으나','다른','낮은','등에','한','수준으로','이를','명까지','것이라고','하지만','들어','가장','후','다시','수준을','등은','수준이','기준으로','매우','것은','수준의','가정을','한다는','보고','대신','사용할','등이','이런','당시','것이다','불구하고','전체','가지고','통해','이나','수준','있으며','경향이','이미','많은','계속','보인다','특히','사람들이','명이','있어','부담을','주요','명에서','명으로','전','주','총','중','있고','년간','일','인','될','월','원','대상으로','있는데','세','로','있도록','등을','프랑스는','낳는','있다는','프랑스','스웨덴','잘','한다고','새로운','이민','독일','데','대해서는','하고','모든','있게','모두','결과','한국은','보면','하지','않은','일반','기준','명의','되면','없는','추가','지속적으로','일을','부모가','확대','할','최대','학교','년에','년에는','일가정','가능','위한','지속','많이','볼','구매','시','이상','이상의','따른','이다','있지만','많다','낳지','또','세계','되고','서비스','공식','어느','국가가','중국','두','이유는','때문이다','있기','않을','것이라는','인당','떨어졌다','정부가','지난','기존의','더욱','역대','명에','명대로','지난해','그런데','올해','분기','명대','출처','하나','안','우리','좋은','세계에서','메뉴','편집','안내','문서','문서의','내용은''입니다','문서를','참고하십시오','목차','관련','보기','러시아','각종','상승','보는','사람','변화','없을','못한','높다','있습니다','자세한','등록','이동','링크','토론','제차','대전','싱가포르','나','다','북한','내용','첫','필요한','포함한','이용','개인정보처리방침','소개','통계','모바일','최근','검색','로그인','개','다운로드','항목','판''되지','일에','확인함','관한','중심으로','한국은행','것','아니라','다음','대','않았다','세대가','이용할','있을','직접','수정','합니다','번','문단을','부분을','본','한다','함께','실제','즉','다음과','않으면','그래서','해도','정도로','심지어','사람들은','거의','해서','않는','경우도','사람이','너무','상황이다','그런','동시에','제대로','편이다','비율','없다','삶의','대부분의','사실','못','지금','것이고','이유로','줄','이들','어려운','먼저','이유','역시','했다','코로나','가능성이','않다','되어','돈을','위해서는','수는','당장','보고서','표''닫기','개요','가지','아예','필요가','있다고','것도','시간이','아니다','아직','현재의','사실상','경우가','차이가','바로','된다','합의사항','이제','갈수록','것에','현','결국','건','발표한','않는다','않고','국회','대통령','콘텐츠','사용','방송','프로그램','기사','시간','서울','문단','이전','기타','영상','현재','자체가','자신의','점점','같다','못하는','받는','수밖에','나오는','양립','국제','인용','위','인권','개선','된','채용','하락','강화','시작','질','활동','기본','분야','대폭','주거','억','통한','전국','연합뉴스','선택','조','의견','성질','상품','도입','우리나라의','뉴스','방안','이미지가','대응','윤석열','추진','네이버','유튜브','댓글','논문','위원회','길','기본계획','보도자료','뉴스레터','공지사항','더보기','극복','공유','과제','글로벌','통권','호','그림','본문','바로가기','끝','회원가입','이용안내','기사를','추천','키워드','공유하기','영역','기자','기사본문','카카오톡','이메일','광고','이슈','구독','문의','이번','전체메뉴','팝업','없습니다','배너','있어요','참고문헌','리뷰','인증','가능합니다','기관','신청','싸이티지','모달','버튼','사진','레이어','이미지','하단','상단','우측','포토','동일','조회','편집패널','기사면','댓글삭제','기사보내기','오피니언','전체기사','비밀번호','제목','리스트','윤','이름','연합인증','라벨','종이책','새창이동']  # 여기에 제외할 단어들을 추가하세요

def get_search_results(query, num_results):
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if 'url=' in href:
                link = href.split('url=')[1].split('&')[0]
                if not (link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif') or link.endswith('.pdf') or link.endswith('.mp4') or 'vimeo.com' in link or 'instagram.com' in link or 'imgur.com' in link or 'download' in link or 'attachment' in link or 'down.do' in link or 'google.com' in link or 'youtube.com' in link):
                    links.append(urllib.parse.unquote(link))
        return links
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
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        article_content = ''
        tags_to_extract = [
            'p', 'div', 'article', 'section', 'header', 'footer', 'nav', 'aside',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'code',
            'li', 'a', 'summary', 'span', 'strong', 'td'
        ]
        for tag_name in tags_to_extract:
            for tag in soup.find_all(tag_name):
                article_content += extract_text_from_tag(tag) + ' '
        return article_content
    except requests.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        return None

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^가-힣\s]', '', text)  # 한글과 공백을 제외한 모든 문자를 제거
    text = re.sub(r'\s+', ' ', text)  # 연속된 공백을 단일 공백으로 변환
    return text

def extract_words(text):
    words = text.split()
    return words

def analyze_content(content):
    preprocessed_text = preprocess_text(content)
    words = extract_words(preprocessed_text)
    word_counts = Counter(words)
    return word_counts

def filter_words(word_counts, min_count, exclude_words):
    # 제외할 단어 리스트를 포함하여 필터링
    filtered_counts = {word: count for word, count in word_counts.items() if count >= min_count and word not in exclude_words}
    return filtered_counts

if __name__ == "__main__":
    query = "저출산"
    
    search_results = get_search_results(query, 100)
    total_word_counts = Counter()
    
    if search_results:
        for url in search_results:
            print(f"\n크롤링 중인 URL: {url}")
            content = crawl_article(url)
            if content:
                word_counts = analyze_content(content)
                total_word_counts.update(word_counts)
            else:
                print("크롤링된 내용이 없습니다.")
    
    min_count = 30
    filtered_word_counts = filter_words(total_word_counts, min_count, EXCLUDE_WORDS)
    
    print(f"\n{query}에 관한 총 단어 발생 횟수 ({min_count}회 이상):")
    for word, count in filtered_word_counts.items():
        print(f"'{word}': {count}")
    
    time.sleep(0.3)
