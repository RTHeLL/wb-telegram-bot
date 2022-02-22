import requests
from telebot import types

from bot import bot, users, command_to_parser_action_dict, bot_logger


@bot.message_handler(commands=['get_brand', 'get_title'])
def get_brand(message) -> None:
    users[message.from_user.id] = {'state': message.text}
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, 'Enter the article number:', reply_markup=markup)
    bot.register_next_step_handler(message, get_article)


def get_article(message) -> None:
    user_id = message.from_user.id
    user_state = users.setdefault(user_id, {'state', None}).copy().get('state')
    article = message.text
    if not isinstance(article, int) and not article.isdigit():
        bot.send_message(message.chat.id, 'Article must be an integer')
        return bot.register_next_step_handler(message, get_article)
    try:
        result = command_to_parser_action_dict[user_state](article)
        bot.reply_to(message, result)
        users[user_id]['state'] = None
    except requests.exceptions.RequestException as exc:
        bot_logger.critical(exc)
        bot.send_message(message.chat.id, 'Error connecting to WildBerries. Contact the administrator (@kinderplayer)')
