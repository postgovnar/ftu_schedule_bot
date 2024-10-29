from functions.visible_webpage_text import visible_webpage_text


def parse_schedule(group_url):
    try:

        a = visible_webpage_text(group_url).split("  ")
        a = list(filter(None, a))
        a = a[a.index('Группа:') + 1:]
        group = a[0].split(" ")[1]
        a = a[a.index('Учебный год:') + 1:]
        year = a[0].split(" ")[0]
        week_info = a[1].split("(")
        week_number = int(week_info[0])
        is_even = week_info[1] == "чётная неделя)"

        a = a[a.index('Тип Недели1') + 1: a.index(' Загрузка…')]

        week_schedule = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': []
        }

        days = {
            'Понедельник': 'monday',
            'Вторник': 'tuesday',
            'Среда': 'wednesday',
            'Четверг': 'thursday',
            'Пятница': 'friday',
            'Суббота': 'saturday'
        }
        current_day = 'monday'
        for i in a:
            if i.replace(" ", "") in days.keys():
                current_day = days[i.replace(" ", "")]
            else:
                week_schedule[current_day].append(i)
        return {
            "is_even": is_even,
            "group": group,
            "schedule": week_schedule
        }
    except Exception:
        raise IOError("Проблема с подключением к сайту вуза, попробуйте еще раз")

