from functions.parse_schedule import parse_schedule


class WeekSchedule:
    def __init__(self, url):
        self.schedule = parse_schedule(url)
        self.even = EvenNotEvenWeekSchedule(self.schedule, even=True)
        self.not_even = EvenNotEvenWeekSchedule(self.schedule, even=False)

    def __str__(self):
        return f'even: {self.even} \n not_even: {self.not_even}'

    def show(self, current: bool):
        if self.schedule:
            is_even = 'чёт'
        else:
            is_even = 'нечёт'
        if current:
            week_value = self.schedule["is_even"]
        else:
            week_value = not self.schedule["is_even"]
        if week_value:
            return f'*Расписание на эту неделю({is_even}):*\n\n{self.even.show()}'
        else:
            return f'*Расписание на эту неделю({is_even}):*\n\n{self.not_even.show()}'


class EvenNotEvenWeekSchedule:
    def __init__(self, schedule, even):
        schedule = schedule['schedule']
        self.monday = DaySchedule(schedule, day='monday', even=even)
        self.tuesday = DaySchedule(schedule, day='tuesday', even=even)
        self.wednesday = DaySchedule(schedule, day='wednesday', even=even)
        self.thursday = DaySchedule(schedule, day='thursday', even=even)
        self.friday = DaySchedule(schedule, day='friday', even=even)
        self.saturday = DaySchedule(schedule, day='saturday', even=even)

    def __str__(self):
        return f'monday: {self.monday} \n tuesday: {self.tuesday} \n wednesday: {self.wednesday} \n thursday: {self.thursday} \n friday: {self.friday} \n saturday: {self.saturday} \n'

    def show(self):
        return f'{self.monday.show()}{self.tuesday.show()}{self.wednesday.show()}{self.thursday.show()}{self.friday.show()}{self.saturday.show()}'


class DaySchedule:
    def __init__(self, schedule, day, even):
        self.day = day
        self.first = Class(schedule[day], even, 1)
        self.second = Class(schedule[day], even, 2)
        self.third = Class(schedule[day], even, 3)
        self.fourth = Class(schedule[day], even, 4)
        self.fifth = Class(schedule[day], even, 5)

        temp = {
            '1': self.first,
            '2': self.second,
            '3': self.third,
            '4': self.fourth,
            '5': self.fifth
        }
        to_show = [i.show_ for i in temp.values()]
        for i in range(len(to_show) - 1, -1, -1):
            if True in to_show[0:i] and True in to_show[i + 1: len(to_show)]:
                to_show[i] = True
        for i in temp.keys():
            temp[i].show_ = to_show[int(i) - 1]

    def __str__(self):
        return f"1: {self.first} \n 2: {self.second} \n 3: {self.third} \n 4: {self.fourth} \n 5: {self.fifth}"

    def show(self):
        temp = {
            '1': self.first,
            '2': self.second,
            '3': self.third,
            '4': self.fourth,
            '5': self.fifth
        }
        days = {
            'monday': 'Понедельник',
            'tuesday': 'Вторник',
            'wednesday': 'Среда',
            'thursday': 'Четверг',
            'friday': 'Пятница',
            'saturday': 'Суббота'
        }
        classes = [temp[i] for i in temp.keys() if temp[i].show_]
        day = f"*{days[self.day]}*\n\n"
        for i in classes:
            day += i.show()
        return day


class Class:
    def __init__(self, schedule, even, number):
        self.number = None
        self.time = None
        self.name = None
        self.type = None
        self.lecturer = None
        self.room = None
        self.show_ = None

        time_table = {
            '1': '09:15-10:50',
            '2': '11:10-12:45',
            '3': '13:30-15:05',
            '4': '15:15-16:50',
            '5': '17:00-18:35'
        }
        even_not_even = {
            'чёт': True,
            'нечёт': False
        }

        def load_merged_class(raw_class_, raw_class_2):
            raw_class_ = raw_class_.split(' ')
            raw_class_2 =  raw_class_2.split(' ')

            if not ('ауд.' in raw_class_):
                raw_class_.insert(-2, 'ауд.')
                raw_class_.insert(-2, '-')

            if not ('ауд.' in raw_class_2):
                raw_class_2.insert(-2, 'ауд.')
                raw_class_2.insert(-2, '-')

            self.number = number
            self.time = time_table[str(number)]
            self.name = ' '.join(raw_class_[4:raw_class_.index('ауд.') - 3])
            self.type = raw_class_[raw_class_.index('ауд.') - 3]
            self.lecturer = ' '.join(raw_class_[raw_class_.index('ауд.') - 2: raw_class_.index('ауд.')]) + '/' + ' '.join(raw_class_2[raw_class_2.index('ауд.') - 2: raw_class_2.index('ауд.')])
            self.room = ' '.join(raw_class_[raw_class_.index('ауд.') + 1: -1]) + '/' + ' '.join(raw_class_2[raw_class_2.index('ауд.') + 1: -1])
            self.show_ = True

        def load_class(raw_class_):
            raw_class_ = raw_class_.split(' ')
            if not ('ауд.' in raw_class_):
                raw_class_.insert(-2, 'ауд.')
                raw_class_.insert(-2, '-')
            self.number = number
            self.time = time_table[str(number)]
            self.name = ' '.join(raw_class_[4:raw_class_.index('ауд.') - 3])
            self.type = raw_class_[raw_class_.index('ауд.') - 3]
            self.lecturer = ' '.join(raw_class_[raw_class_.index('ауд.') - 2: raw_class_.index('ауд.')])
            self.room = ' '.join(raw_class_[raw_class_.index('ауд.') + 1: -1])
            self.show_ = True

        def load_empty_class():
            self.number = number
            self.time = time_table[str(number)]
            self.name = 'Окно'
            self.type = ''
            self.lecturer = ''
            self.room = ''
            self.show_ = False

        # Находим нужную пару
        raw_class = []
        for i in schedule:
            if i[0] == str(number):
                ind = schedule.index(i)
                raw_class.append(schedule[ind])
                if len(schedule) - 1 == ind:
                    break
                if not schedule[ind + 1][0].isnumeric():
                    raw_class.append(schedule[ind + 1])

        if raw_class:
            if len(raw_class) == 2:
                if raw_class[0].split(' ')[-1] == '*' and raw_class[1].split(' ')[-1] == '*':
                    load_merged_class(raw_class[0], raw_class[1])
                else:
                    if even_not_even[raw_class[0].split(' ')[-1]] == even:
                        load_class(raw_class[0])
                    else:
                        load_class(raw_class[1])
            else:
                if raw_class[0].split(' ')[-1] == '*':
                    load_class(raw_class[0])
                else:
                    if even_not_even[raw_class[-1].split(' ')[-1]] == even:
                        load_class(raw_class[0])
                    else:
                        load_empty_class()
        else:
            load_empty_class()

    def __str__(self):
        return f'{self.number}  {self.time}  {self.name}  {self.type}  {self.lecturer}  {self.room} {self.show_}'

    def show(self):
        if self.type:
            return f'{self.number} пара {self.time}\n{self.name} {self.type}\n{self.lecturer} {self.room}\n\n'
        else:
            return f'{self.number} пара {self.time}{self.name}\n\n'
