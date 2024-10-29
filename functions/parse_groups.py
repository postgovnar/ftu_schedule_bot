from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from database.data_base_functions import add_group
from datetime import date


def parse_groups():
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(string=True)
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def visible_webpage_text(url):
        r = requests.get(url, timeout=50)
        if r.status_code != 200:
            raise Exception(r.status_code)
        r = r.text
        return text_from_html(r)

    temp = []
    for i in range(15000, 21000):
        current_date = date.today()
        current_year = int(current_date.year)
        if current_date.month >= 8:
            sem = 1
        else:
            sem = 2

        if sem == 1:
            education_year = f'{current_year}-{current_year + 1}'
        else:
            education_year = f'{current_year - 1}-{current_year}'

        try:
            group_url = f"https://eios.spbftu.ru/Rasp/Rasp.aspx?group={i}&sem={sem}"
            a = visible_webpage_text(group_url).split("  ")
            a = list(filter(None, a))
            year = a[a.index('Учебный год:') + 1:]
            year = year[0].split(" ")[0]
            print(year)
            group = a[a.index('Группа:') + 1:]
            group = group[0].split(" ")[1]
            if group != 'Ссылка' and year == education_year:
                add_group(group, f"https://eios.spbftu.ru/Rasp/Rasp.aspx?group={i}&sem={sem}")
        except Exception as e:
            print(e)
            temp.append(i)

    print(temp)


parse_groups()
