from bot.bot import bot_app
from configs.config import config

if __name__ == '__main__':
    bot_app(config.token)
    # try:
    #     bot_app(config.token)
    # except Exception as e:
    #     print(e)