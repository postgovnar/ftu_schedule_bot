from database.data_base_functions import get_group_url, get_group_url_by_id
from functions.parse_schedule import parse_schedule

time_table = {
    '1': '09:15-10:50',
    '2': '11:10-12:45',
    '3': '13:30-15:05',
    '4': '15:15-16:50',
    '5': '17:00-18:35'
}
days = {
        'понедельник': 'monday',
        'вторник': 'tuesday',
        'среда': 'wednesday',
        'четверг': 'thursday',
        'пятница': 'friday',
        'суббота': 'saturday'
    }
week_schedule = {
        'monday': [],
        'tuesday': [],
        'wednesday': [],
        'thursday': [],
        'friday': [],
        'saturday': []
        }

day_schedule_template = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': []
    }


def lowercase_no_whitespaces(str_: str):
    return str_.replace(" ", "").lower()



last = ""
def parse_class(raw_class):
    global last
    raw_class = raw_class.split(' ')
    if not 'ауд.' in raw_class:
        raw_class.insert(-2, 'ауд.')
        raw_class.insert(-2, '-')
    if time_table.get(raw_class[0]):
        last = raw_class[0:4]
    else:
        raw_class = last + raw_class
    return {
        'number': raw_class[0],
        'time': time_table.get(raw_class[0]),
        'name': ' '.join(raw_class[4:raw_class.index('ауд.') - 3]),
        'type': raw_class[raw_class.index('ауд.') - 3],
        'lecturer': ' '.join(raw_class[raw_class.index('ауд.') - 2: raw_class.index('ауд.')]),
        'room': ' '.join(raw_class[raw_class.index('ауд.') + 1: -1]),
        'even': raw_class[-1]

    }



def get_week_schedule(user_id, current: bool):
    week_schedule_ = {
        'monday': {
            'even': [],
            'not_even': []
        },
        'tuesday': {
            'even': [],
            'not_even': []
        },
        'wednesday': {
            'even': [],
            'not_even': []
        },
        'thursday': {
            'even': [],
            'not_even': []
        },
        'friday': {
            'even': [],
            'not_even': []
        },
        'saturday': {
            'even': [],
            'not_even': []
        }

    }
    group_url = get_group_url_by_id(user_id)
    schedule_info = parse_schedule(group_url)

    raw_schedule = schedule_info["schedule"]
    temp = 0
    while temp < len(raw_schedule) - 1:
        if days.get(lowercase_no_whitespaces(raw_schedule[temp])):
            current_day_to_parse = days.get(lowercase_no_whitespaces(raw_schedule[temp]))
            temp += 1
            while not days.get(lowercase_no_whitespaces(raw_schedule[temp])):
                week_schedule[current_day_to_parse].append(parse_class(raw_schedule[temp]))
                temp += 1
                if temp == len(raw_schedule):
                    break
        else:

            raise Exception("Что-то с парсом расписания")


    for day in days.values():
        temp_even = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': []
    }
        temp_not_even = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': []
    }
        for class_ in week_schedule.get(day):
            if class_['even'] == '*':
                temp_even[class_['number']].append(class_)
                temp_not_even[class_['number']].append(class_)
            elif class_['even'] == 'чёт':
                temp_even[class_['number']].append(class_)
                temp_not_even[class_['number']].append(window(class_['number']))
            else:
                temp_even[class_['number']].append(window(class_['number']))
                temp_not_even[class_['number']].append(class_)
        week_schedule_[day]['even'] = temp_even
        week_schedule_[day]['not_even'] = temp_not_even

    if current:
        week_value = schedule_info["is_even"]
    else:
        week_value = not schedule_info["is_even"]
    even_week = []
    not_even_week = []
    for i in week_schedule_.keys():
        even_week.append(week_schedule_[i]['even'])
        not_even_week.append(week_schedule_[i]['not_even'])

    if week_value:
        return even_week
    else:
        return not_even_week



def window(number):
    return {
        'number': number,
        'time': time_table.get(number),
        'name': 'Окно',
        'type': '',
        'lecturer': '',
        'room': '',
        'even': ''

    }


def get_day_schedule(user_id, current: bool, day):
    return get_week_schedule(user_id, current)[day]