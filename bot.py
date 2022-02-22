import telebot

import config
import logging

from classes.parsers import HTMLParser, JSONParser

html_parser = HTMLParser()
json_parser = JSONParser()

users = dict()
command_to_parser_action_dict = {
    '/get_brand': html_parser.get_brand,
    '/get_title': json_parser.get_title
}

bot = telebot.TeleBot(config.TG_TOKEN)

logging.basicConfig(filename='logs.log',
                    filemode='w+',
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    datefmt='%d-%m-%Y [%H:%M:%S]',
                    level=logging.ERROR)
bot_logger = telebot.logger
