import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import textProcessing

def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text   # Вернем данные объекта text
    return ''

def csv_read(data):
    with open("data.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['group_name'], data['song_title'], data['text']))

def cut_str(str):
    return str[0:str.rindex('/')+1]

def get_link(html, template):
    if html == '':
        return None

    soup = BeautifulSoup(html, 'lxml')
    link = soup.find('table').find_all('a')

    links = []
    for i in link:
        if i.get('href').startswith('http://') == False and \
                        i.get('href').find('..') == -1 and \
                        i.get('href').endswith('.html') == True:
            link = template + i.get('href')
            links.append(link)
    return links

def get_txt(html, f):
    soup = BeautifulSoup(html, 'lxml')
    # Ищем название группы
    group_name = soup.find('table').find('td', class_='h3').text.strip()
    # Ищем название песни
    song_title = soup.find('table',cellpadding="10").find('h1').string
    # получаем текст песни
    text = soup.find('table',cellpadding="10").find('font').text
    # Разбиваем текст песни на слова
    words, tokensCount = textProcessing.parseText(text)
    # записываем в файл
    f.write(group_name + '; ' + song_title + '; ' + str(words) + '\n')

    # data = {'group_name': group_name, 'song_title': song_title, 'text': words}
    # return data


def parser():
    start_time = datetime.now()
    print (start_time)

    url = 'http://woos.ru/index.html'

    group_links = []
    group_links.extend(get_link(get_html(url), cut_str(url)))
    print('количество групп: ' + str(len(group_links)))
    print(datetime.now() - start_time)

    alb_links = []
    for link in group_links:
        alb_links.extend(get_link(get_html(link),cut_str(link)))
    group_links = None
    print('количество альбомов: ' + str(len(alb_links)))
    print(datetime.now() - start_time)

    text_links = []
    for link in alb_links:
        text_links.extend(get_link(get_html(link),cut_str(link)))
    alb_links = None
    print('количество песен: ' + str(len(text_links)))
    print(datetime.now() - start_time)

    f = open("data_1.txt","w+")
    i = 0
    # texts = []
    time_ = datetime.now()
    for link in text_links:
        i += 1
        if i%100 == 0:
            print(str(i) + ' : ' + str(datetime.now() - time_))
            print()
        html = get_html(link)
        if html != '':
            get_txt(html, f)
    f.close()
    print(datetime.now() - start_time)

parser()

# alb = get_link(get_html(group_links[0]),cut_str(group_links[0]))
# text_links = get_link(get_html(alb[0]),cut_str(alb[0]))
# txt = get_txt(get_html(text_links[0]), f)

# corpus = []
# for d in texts:
#     corpus.append(d['text'])
# res = textToWords.tf_idf(corpus)
# print(res[0:3])
# print(datetime.now() - start_time)


