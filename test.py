from binance.client import Client
from binance.enums import *
import time
# telegram_bot.apps.TelegramBotConfig
import os
import django

from config import *
# from telegram import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.telegram_bot.settings')
django.setup()

# Enter your API key and secret key here
client = Client(api_key=api_key, api_secret=secret_key, testnet=True)

# Define trading parameters
symbol = 'ETHUSDT'
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