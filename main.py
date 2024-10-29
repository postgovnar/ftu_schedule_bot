import sys
from bot.bot import bot_app
from bot.bot_alerts import bot_start_alert, bot_stop_alert
from configs.config import config
import time
from time_events.daily_weekly_messaging import weekly_daily_messaging
import telebot


if __name__ == '__main__':
    bot = telebot.TeleBot(config.token)
    bot_start_alert(bot)
    while True:
        try:
            bot_app(bot)
            weekly_daily_messaging(bot)
        except Exception as e:
            if e == SystemExit:
                bot_stop_alert(bot)
                time.sleep(1000)
                sys.exit()
            time.sleep(15)
