from functions.parse_schedule import parse_schedule


class WeekSchedule:
    def __init__(self, url):
        self.ex = False
        try:
            self.schedule = parse_schedule(url)
        except IOError as e:
            self.ex = True
            print(e)
            self.schedule = {'is_even': True, 'group': 'ЛПб-РТС-24-1', 'schedule': {'monday': ['1 пара 09:15 10:50 Физическая культура и спорт Пр. Лешева Н.С. ауд. Открытый стадион *', '2 пара 11:10 12:45 История России Лек. Добрякова Н.А. ауд. 2.409 *', '3 пара 13:30 15:05 Ознакомительный практикум Пр. Басова Е.Н. ауд. 2.133 чёт', '4 пара 15:15 16:50 Информатика Лаб. Мартын К.А. ауд. 1.310 *'], 'tuesday': ['1 пара 09:15 10:50 Начертательная геометрия и инженерная графика Пр. Вохмянин Н.А. ауд. 2.210 чёт', 'Начертательная геометрия и инженерная графика Лек. Вохмянин Н.А. ауд. 2.410 нечёт', '2 пара 11:10 12:45 Начертательная геометрия и инженерная графика Пр. Вохмянин Н.А. ауд. 2.210 *', '3 пара 13:30 15:05 История России Пр. Добрякова Н.А. ауд. 2.416 *', '4 пара 15:15 16:50 Иностранный язык Пр. Бекмурзаева Ф.Ш. ауд. 1.436 *'], 'wednesday': ['1 пара 09:15 10:50 Основы российской государственности Лек. Петров В.Н. ауд. 1.231 чёт', 'Межкультурное взаимодействие в современном мире Лек. Михайлова А.И. ауд. 1.054 нечёт', '2 пара 11:10 12:45 Математика Лек. Затенко С.И. ауд. 2.409 *', '3 пара 13:30 15:05 Основы российской государственности Пр. Филинова И.В. ауд. 1.247 нечёт', '4 пара 15:15 16:50 Физическая культура и спорт\nЛекционные занятия с 02.10 Пр./Лек. Лешева Н.С., Бахтина Т.Н. ауд. Открытый стадион / 3.033 *'], 'thursday': ['1 пара 09:15 10:50 История России Пр. Добрякова Н.А. ауд. 2.416 чёт', 'Управление личным временем Лек. Косоногова Е.С. ауд. 1.318 нечёт', '2 пара 11:10 12:45 Физика Лаб. Былев А.Б. ауд. 1.025 чёт', '3 пара 13:30 15:05 Математика Пр. Затенко С.И. ауд. 2а.352 *', '4 пара 15:15 16:50 Управление личным временем Пр. Косоногова Е.С. ауд. 1.247 чёт', 'Физика Пр. Совтус Н.В. ауд. 1.026 нечёт', '5 пара 17:00 18:35 История России Пр. Добрякова Н.А. ауд. 2.416 *'], 'friday': ['1 пара 09:15 10:50 Информатика Лек. Васильев Н.П. ауд. 1.101 чёт', 'Основы российской государственности Пр. Филинова И.В. ауд. 1.245 нечёт', '2 пара 11:10 12:45 Основы робототехники Лек. Захаров И.В. ауд. 1.231 чёт', 'Физика Лек. Былев А.Б. ауд. 1.010 нечёт', '3 пара 13:30 15:05 Основы робототехники Пр. Захаров И.В. ауд. 1.091 *', '4 пара 15:15 16:50 Межкультурное взаимодействие в современном мире Пр. Михайлова А.И. ауд. 1.213 нечёт'], 'saturday': ['3 пара 13:30 15:05 21 и 28 Сентября с 12:55 до 16:05, группа занимается социально-ознакомительным практикумом в структурном подразделении СПбГЛТУ Парк ЛТА. *']}}
        self.even = EvenNotEvenWeekSchedule(self.schedule, even=True, ex=self.ex)
        self.not_even = EvenNotEvenWeekSchedule(self.schedule, even=False, ex=self.ex)

    def __str__(self):
        return f'even: {self.even} \n not_even: {self.not_even}'

    def show(self, current: bool):
        if self.ex:
            return "Проблема с подключением к сайту вуза, попробуйте еще раз позже"
        if current:
            week_value = self.schedule["is_even"]
        else:
            week_value = not self.schedule["is_even"]
        if week_value:
            return f'*Расписание на неделю({'чёт'}):*\n\n{self.even.show()}'
        else:
            return f'*Расписание на неделю({'нечёт'}):*\n\n{self.not_even.show()}'


class EvenNotEvenWeekSchedule:
    def __init__(self, schedule, even, ex):
        self.ex = ex
        schedule = schedule['schedule']
        self.monday = DaySchedule(schedule, day='monday', even=even, ex=self.ex)
        self.tuesday = DaySchedule(schedule, day='tuesday', even=even, ex=self.ex)
        self.wednesday = DaySchedule(schedule, day='wednesday', even=even, ex=self.ex)
        self.thursday = DaySchedule(schedule, day='thursday', even=even, ex=self.ex)
        self.friday = DaySchedule(schedule, day='friday', even=even, ex=self.ex)
        self.saturday = DaySchedule(schedule, day='saturday', even=even, ex=self.ex)

    def __str__(self):
        return f'monday: {self.monday} \n tuesday: {self.tuesday} \n wednesday: {self.wednesday} \n thursday: {self.thursday} \n friday: {self.friday} \n saturday: {self.saturday} \n'

    def show(self):
        return f'{self.monday.show()}{self.tuesday.show()}{self.wednesday.show()}{self.thursday.show()}{self.friday.show()}{self.saturday.show()}'


class DaySchedule:
    def __init__(self, schedule, day, even, ex):
        self.ex = ex
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
        if self.ex:
            return "Проблема с подключением к сайту вуза, попробуйте еще раз позже"

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
        schedule = ''
        for i in classes:
            schedule += i.show()
        if schedule:
            day_schedule = day + schedule
            return day_schedule




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
            self.name = '\nОкно'
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
