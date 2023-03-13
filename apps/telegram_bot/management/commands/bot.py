from telebot import TeleBot
from config import *
from binance.client import Client
import time

bot = TeleBot(tg_token, threaded=False)


symbol = "ETHUSDT"
client = Client(api_key=api_key, api_secret=secret_key, testnet=True)
rsi = RSI(client = client, symbol = symbol, interval="1m", period=3)

client.futures_change_leverage(leverage=10, symbol=symbol)
orders = 5
orders_buy = 0
scope = False
while True:
    rsi.update_status()

    if (rsi.value < 45 and scope == False and orders > orders_buy):
        order = client.futures_create_order(symbol=symbol, side="BUY", positionSide="LONG", type="MARKET", quantity=0.1)
        print(1)
        rsi.print_info()
        orders_buy += 1
        scope = True

    elif (rsi.value < 45 and rsi.value > rsi.last_valueand& orders > orders_buy):
        order = client.futures_create_order(symbol=symbol, side="BUY", positionSide="LONG", type="MARKET", quantity=0.1)
        print(2)
        rsi.print_info()
        orders_buy += 1

    elif (rsi.value < 45 and orders > orders_buy):
        order = client.futures_create_order(symbol=symbol, side="BUY", positionSide="LONG", type="MARKET", quantity=0.1)
        print(3)
        rsi.print_info()
        orders_buy += 1
    
    time.sleep(10)


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