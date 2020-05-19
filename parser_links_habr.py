import requests
from bs4 import BeautifulSoup
import sqlite3


URL = 'https://habr.com/ru/hub/python/'
HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36', 'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='post post_preview')
    habs = []
    for item in items:
        habs.append({
            'link': item.find('a', class_='post__title_link').get('href'),
        })
    return habs




def save_file_db(items):
    conn = sqlite3.connect('db-bot.sqlite')
    cursor = conn.cursor()
    db_list = []
    hub_list = []
    for row in cursor.execute('SELECT link from Hab ORDER BY link'):
        db_list.append(row)
    for item in items:
        hub_list.append(item['link'])
    db_list1 = [''.join(ele) for ele in db_list]
    result = list(set(hub_list) - set(db_list1))
    res = [tuple(result[i:i + 1]) for i in range(0, len(result))]
    try:
        cursor.executemany("insert into Hab values (Null, ?);", res)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()
    conn.close()



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        habs = []
        print('Парсинг страницы...')
        html = get_html(URL)
        habs.extend(get_content(html.text))
        save_file_db(habs)
        print(f'Получено {len(habs)} ссылок')
    else:
        print('Error')

parse()
