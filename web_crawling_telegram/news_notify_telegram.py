# hjtest_1_bot
import configparser
import telegram
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
...

#서치 키워드
search_word = '단독'

#텔레그램 봇 생성
BOT_TOKEN=config('BOT_TOKEN')

bot = telegram.Bot(token=BOT_TOKEN)
chat_id=config('chat_id')

#기존에 보냈던 링크를 담아둘 리스트
old_links = []

#링크 추출 함수
def extract_links(old_links=[]):
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={search_word}'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')
    news_list = search_result.select('.bx > .news_wrap > a')

    links = []
    for news in news_list[:5]:
        link = news['href']
        links.append(link)

    new_links=[]
    for link in links:
        if link not in old_links:
            new_links.append(link)
    print(new_links)

    return new_links

#이전 링크를 매개변수로 받아서 비교 후, 새로운 링크만 출력
#차후 이 부분을 메세지 전송 코드로 변경하고 매시간 동작하도록 설정
#새로운 링크가 없다면 빈 리스트 반환
def send_links():
    global old_links
    new_links = extract_links(old_links)
    if new_links:
        for link in new_links:
            bot.sendMessage(chat_id=chat_id, text = link)
    else:
        bot.sendMessage(chat_id=chat_id, text = '새로운 단독 뉴스 없음')
    old_links += new_links.copy()
    old_links = list(set(old_links))

#최초 시작
send_links()
