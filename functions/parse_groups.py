from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from database.data_base_functions import add_group


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
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(r.status_code)
        r = r.text
        return text_from_html(r)

    cnt = 0
    temp = []
    b = []
    for i in [17560, 17948, 17949, 18048, 18049, 18353, 18354, 18562, 18563, 18759]:
        if i % 100 == 0:
            print(i)
        try:
            group_url = f"https://eios.spbftu.ru/Rasp/Rasp.aspx?group={i}&sem=1"
            a = visible_webpage_text(group_url).split("  ")
            a = list(filter(None, a))
            a = a[a.index('Группа:') + 1:]
            group = a[0].split(" ")[1]
            if group != 'Ссылка':
                add_group(group, f"https://eios.spbftu.ru/Rasp/Rasp.aspx?group={i}&sem=1")
                cnt += 1
                print(f"Групп добавлено {cnt} {group}")
        except Exception as e:
            print(e)
            temp.append(i)

    print(temp)

parse_groups()
