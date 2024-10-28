from bot.bot import bot_app
from configs.config import config
import time
from time_events.daily_weekly_messaging import weekly_daily_messaging
import telebot


if __name__ == '__main__':
    bot = telebot.TeleBot(config.token)
    while True:
        try:
            bot_app(bot)
            weekly_daily_messaging(bot)
        except Exception as e:
            time.sleep(15)
