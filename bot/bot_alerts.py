from database.data_base_functions import get_users_id


def bot_start_alert(bot):
    for i in get_users_id():
        bot.send_message(i, "Бот снова функционирует, спасибо за ожидание")


def bot_stop_alert(bot):
    for i in get_users_id():
        bot.send_message(i, "Бот закрывается на добаботку. Просим прощения")
