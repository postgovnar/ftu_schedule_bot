import telebot
from telebot import types
from configs.config import main_send_text_config, main_answer_text_config, register_answer_text_config, register_send_text_config
from database.data_base_functions import *
from functions.get_schedule import get_week_schedule
from functions.new_get_schedule import WeekSchedule


def bot_app(token: str):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, register_send_text_config.start_message_0)
        bot.send_message(message.chat.id, register_send_text_config.start_message_1)
        bot.send_message(message.chat.id, register_send_text_config.group_add_hint)


    @bot.message_handler(func= lambda message: message.text in get_group_names())
    def register_user_start(message):
        user_data = {
            'user_id': message.from_user.id,
            'user_name': message.from_user.username,
            'user_group': message.text,
            'weekly_messaging': None,
            'daily_messaging': None
        }

        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(register_answer_text_config.weekly_messaging_yes))
        markup.row(types.KeyboardButton(register_answer_text_config.weekly_messaging_no))

        bot.send_message(message.from_user.id, register_send_text_config.group_added)
        bot.send_message(message.from_user.id, register_send_text_config.weekly_messaging, reply_markup=markup)

        bot.register_next_step_handler(message, register_user, user_data)


    @bot.message_handler(func= lambda message: message.text in register_answer_text_config.__dict__.values())
    def register_user(message, user_data):
        if message.text in (register_answer_text_config.weekly_messaging_yes, register_answer_text_config.weekly_messaging_no):
            user_data['weekly_messaging'] = message.text == register_answer_text_config.weekly_messaging_yes

            markup = types.ReplyKeyboardMarkup()
            markup.row(types.KeyboardButton(register_answer_text_config.daily_messaging_yes))
            markup.row(types.KeyboardButton(register_answer_text_config.daily_messaging_no))

            bot.send_message(message.from_user.id, register_send_text_config.daily_messaging, reply_markup=markup)
            bot.register_next_step_handler(message, register_user, user_data)

        elif message.text in (register_answer_text_config.daily_messaging_yes, register_answer_text_config.daily_messaging_no):
            user_data['daily_messaging'] = message.text == register_answer_text_config.daily_messaging_yes

            add_user(user_data)

            bot.send_message(message.from_user.id, register_send_text_config.end_registration)

            markup = types.ReplyKeyboardMarkup()
            markup.row(types.KeyboardButton(main_answer_text_config.main_button_day))
            markup.row(types.KeyboardButton(main_answer_text_config.main_button_week))
            markup.row(types.KeyboardButton(main_answer_text_config.main_button_support_roadmap))
            markup.row(types.KeyboardButton(main_answer_text_config.main_button_donate))

            bot.send_message(message.from_user.id, main_send_text_config.main_message, reply_markup=markup)
            bot.register_next_step_handler(message, main)




    @bot.message_handler(func= lambda message: message.text in main_answer_text_config.__dict__.values())
    def main(message):
        if message.text == main_answer_text_config.main_button_day:

            markup = types.ReplyKeyboardMarkup()
            for i in main_answer_text_config.days_of_week:
                markup.row(types.KeyboardButton(i))

            bot.reply_to(message, main_send_text_config.choose_day)

        elif message.text == main_answer_text_config.main_button_week:
            markup = types.ReplyKeyboardMarkup()
            markup.row(types.KeyboardButton(main_answer_text_config.current_week))
            markup.row(types.KeyboardButton(main_answer_text_config.next_week))

            bot.reply_to(message, main_send_text_config.choose_week, reply_markup=markup)


        elif message.text == main_answer_text_config.main_button_support_roadmap:
            bot.send_message(message.chat.id, main_send_text_config.support_roadmap)

        elif message.text == main_answer_text_config.main_button_donate:
            bot.send_message(message.chat.id, main_send_text_config.donate)

        elif message.text in (main_answer_text_config.current_week, main_answer_text_config.next_week):
            week_schedule(message, message.text == main_answer_text_config.current_week)
        elif message.text in main_answer_text_config.days_of_week:
            bot.send_message(message.from_user.id, 'функция не готова')

    def week_schedule(message, current: bool):
        schedule = WeekSchedule(get_group_url_by_id(message.from_user.id))
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(main_answer_text_config.main_button_day))
        markup.row(types.KeyboardButton(main_answer_text_config.main_button_week))
        markup.row(types.KeyboardButton(main_answer_text_config.main_button_support_roadmap))
        markup.row(types.KeyboardButton(main_answer_text_config.main_button_donate))


        bot.send_message(message.from_user.id, schedule.show(current) , reply_markup=markup)


    # def day_schedule(message):
    #     pass
    #     # пупупу
    #     # days = {
    #     #     'Понедельник': 'monday',
    #     #     'Вторник': 'tuesday',
    #     #     'Среда': 'wednesday',
    #     #     'Четверг': 'thursday',
    #     #     'Пятница': 'friday',
    #     #     'Суббота': 'saturday'
    #     # }
    #     # day = days[message.text]
    #     #
    #     # bot.send_message(message.chat.id, get_day_schedule())
    # def week_schedule(message):
    #     current = message.text == "Текущая неделя"
    #     bot.send_message(message.chat.id, get_week_schedule(message.from_user.id, current))

    @bot.message_handler(func= lambda message: message.text)
    def error(message):
        bot.send_message(message.from_user.id, main_send_text_config.error_message)

    bot.polling(non_stop=True, interval=0)



