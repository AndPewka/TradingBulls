from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from apps.telegram_bot.models import *
from os import getenv

bot = TeleBot(getenv("TELEGRAM_TOKEN"), threaded=False)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет")

class Command(BaseCommand):
    help = 'Bot' 

    def handle(self, *args, **kwargs):
        pass
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()