import threading
import time
import datetime
import pytz
from database.data_base_functions import daily_messaging_users_id, weekly_messaging_users_id, get_group_url_by_id
from functions.get_schedule import WeekSchedule
from configs.config import main_send_text_config
moscow_tz = pytz.timezone('Europe/Moscow')


def daily_messaging(bot):
    users_id = daily_messaging_users_id()
    day = datetime.datetime.now(moscow_tz).weekday()
    for user_id in users_id:
        schedule = WeekSchedule(get_group_url_by_id(user_id))
        current = schedule.schedule['is_even']
        if current:
            days = {
                0: schedule.even.monday.show(),
                1: schedule.even.tuesday.show(),
                2: schedule.even.wednesday.show(),
                3: schedule.even.thursday.show(),
                4: schedule.even.friday.show(),
                5: schedule.even.saturday.show()
            }
        else:
            days = {
                0: schedule.not_even.monday.show(),
                1: schedule.not_even.tuesday.show(),
                2: schedule.not_even.wednesday.show(),
                3: schedule.not_even.thursday.show(),
                4: schedule.not_even.friday.show(),
                5: schedule.not_even.saturday.show()
            }
        message = days.get(day)
        if message:
            try:
                bot.send_message(users_id, main_send_text_config.daily_messaging, parse_mode="Markdown")
                bot.send_message(users_id, message, parse_mode="Markdown")
            except Exception as e:
                print(e)


def weekly_messaging(bot):
    users_id = weekly_messaging_users_id()
    for user_id in users_id:
        schedule = WeekSchedule(get_group_url_by_id(user_id))
        current = schedule.schedule['is_even']
        message = schedule.show(not current)
        if message:
            try:
                bot.send_message(users_id, main_send_text_config.weekly_messaging, parse_mode="Markdown")
                bot.send_message(users_id, message, parse_mode="Markdown")
            except Exception as e:
                print(e)


def wait_until_next_trigger(bot):
    while True:
        now = datetime.datetime.now(moscow_tz)
        if now.weekday() < 5:
            next_trigger = now.replace(hour=7, minute=30, second=0, microsecond=0)
            if now >= next_trigger:
                next_trigger += datetime.timedelta(days=1)
            time_to_sleep = (next_trigger - now).total_seconds()
            time.sleep(time_to_sleep)
            daily_messaging(bot)
        elif now.weekday() == 5:
            if now.hour < 7 or (now.hour == 7 and now.minute < 30):
                next_trigger = now.replace(hour=7, minute=30, second=0, microsecond=0)
            elif now.hour < 13 or (now.hour == 13 and now.minute == 0):
                next_trigger = now.replace(hour=13, minute=0, second=0, microsecond=0)
            else:
                next_trigger = now + datetime.timedelta(days=(7 - now.weekday()))
                next_trigger = next_trigger.replace(hour=7, minute=30, second=0, microsecond=0)

            time_to_sleep = (next_trigger - now).total_seconds()
            time.sleep(time_to_sleep)
            if next_trigger.hour == 7 and next_trigger.minute == 30:
                daily_messaging(bot)
            elif next_trigger.hour == 13 and next_trigger.minute == 0:
                weekly_messaging(bot)
        else:
            next_trigger = now + datetime.timedelta(days=(7 - now.weekday()))
            next_trigger = next_trigger.replace(hour=7, minute=30, second=0, microsecond=0)
            time_to_sleep = (next_trigger - now).total_seconds()
            time.sleep(time_to_sleep)
            daily_messaging(bot)


def weekly_daily_messaging(bot):
    threading.Thread(target=wait_until_next_trigger, args=(bot,), daemon=True).start()


